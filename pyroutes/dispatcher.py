import pyroutes

from pyroutes.http.request import Request
import pyroutes.settings as settings

class Dispatcher(object):

    def create_middleware_chain(self, handler, request):
        chain = handler
        for full_path in settings.MIDDLEWARE:
            module_name, class_name = full_path.rsplit('.', 1)

            module = __import__(module_name, fromlist=[class_name])
            middleware = getattr(module, class_name)

            chain = middleware(chain)

        return chain(request)

    def dispatch(self, environ, start_response):
        # Update site root value so pyroutes can make root-relative path redirects
        if not hasattr(settings, 'SITE_ROOT'):
            settings.SITE_ROOT = environ.get('SCRIPT_NAME', '').rstrip('/')

        request = Request(environ)
        handler = self.find_request_handler(environ['PATH_INFO'])
        response = self.create_middleware_chain(handler, request)
        headers = self._combine_headers(response)
        start_response(response.status_code, headers)

        if isinstance(response.content, basestring):
            return [response.content]
        else:
            return response.content

    def find_request_handler(self, current_path):
        """
        Locates the handler for the specified path. Return None if not found.
        """

        # If we don't have a current path, look for the root handler.
        # See issue #2 <http://github.com/pyroutes/pyroutes/issues/2>
        if current_path == '':
            current_path = '/'

        complete_path = current_path.rstrip('/')
        if not current_path.endswith('/'):
            current_path += '/'

        while current_path != '/':
            current_path = current_path[:current_path.rfind('/')] or '/'
            if current_path in pyroutes.__request__handlers__:
                handler = pyroutes.__request__handlers__[current_path]
                argument_count = self._get_argument_count(complete_path, current_path)
                if self._match_with_arguments(handler, argument_count):
                    return handler

    def _get_argument_count(self, complete_path, current_path):
        """
        Returns the number of URL elements left over for between
        the current path and the complete path.
        """
        complete_path_comps = complete_path.rstrip('/').split('/')
        current_path_comps = current_path.rstrip('/').split('/')
        return len(complete_path_comps) - len(current_path_comps)

    def _match_with_arguments(self, handler, arg_count):
        """
        Returns True if the number of remaining URL elements for
        the tested handler matches the number of arguments for the
        handler. It also tries to match against handlers with defaults
        on their arguments.
        """
        if hasattr(handler, 'im_func'):
            return self._match_handler_arguments(handler.im_func, arg_count, 2)
        else:
            return self._match_handler_arguments(handler, arg_count, 1)

    def _match_handler_arguments(self, handler, arg_count, obligatories):
        """
        Helper method for `_match_with_arguments` for dealing with
        function based handlers.

        The "obligatories" argument tells the function how many arguments the
        handler will recieve from a different source. (i.e. classes get self as
        well as the requestpassed to them, functions only the request)
        """
        required_args = handler.handler.func_code.co_argcount - obligatories
        defaults = len(handler.handler.func_defaults or '')
        if arg_count <= required_args <= (defaults + arg_count):
            return True
        return False

    def _combine_headers(self, response):
        """
        Combine "normal" http headers with the cookie headers into single list
        """
        return response.headers + response.cookies.cookie_headers
