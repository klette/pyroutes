import threading
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
        safe_data = threading.local()
        safe_data.request = Request(environ)

        # Update site root value so pyroutes can make root-relative path redirects
        if not hasattr(settings, 'SITE_ROOT'):
            settings.SITE_ROOT = environ.get('SCRIPT_NAME', '').rstrip('/')

        safe_data.handler = self.find_request_handler(environ['PATH_INFO'])

        safe_data.response = self.create_middleware_chain(safe_data.handler,
            safe_data.request)

        safe_data.headers = safe_data.response.headers
        safe_data.headers += safe_data.response.cookies.cookie_headers
        start_response(safe_data.response.status_code, safe_data.headers)

        if isinstance(safe_data.response.content, basestring):
            return [safe_data.response.content]
        else:
            return safe_data.response.content

    def find_request_handler(self, current_path):
        """
        Locates the handler for the specified path. Return None if not found.
        """

        # If we don't have a current path, look or the root handler.
        # See issue #2 <http://github.com/pyroutes/pyroutes/issues/2>
        if current_path == '':
            current_path = '/'

        complete_path = current_path
        handler = pyroutes.__request__handlers__.get(current_path, None)

        while handler is None and current_path:
            if current_path in pyroutes.__request__handlers__:
                handler = pyroutes.__request__handlers__[current_path]
                argument_count = self._get_argument_count(complete_path, current_path)
                if self._match_with_arguments(handler, argument_count):
                    return handler

            current_path = current_path[:current_path.rfind('/')]
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
            return self._match_class_handler_arguments(handler, arg_count)
        else:
            return self._match_function_handler_arguments(handler, arg_count)

    def _match_class_handler_arguments(self, handler, arg_count):
        """
        Helper method for `_match_with_arguments` for dealing with
        class based handlers.
        """
        handler_func = handler.handler.im_func
        if handler_func.func_code.co_argcount - 2 != arg_count:
            if len(handler_func.func_defaults or '') + 1 \
                == handler_func.func_code.co_argcount:
                return True
        return False

    def _match_function_handler_arguments(self, handler, arg_count):
        """
        Helper method for `_match_with_arguments` for dealing with
        function based handlers.
        """
        if handler.handler.func_code.co_argcount - 1 != arg_count:
            if len(handler.handler.func_defaults or '') + 1 == \
                    handler.handler.func_code.co_argcount:
                return True
        return False
