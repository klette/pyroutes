import threading
import pyroutes

from pyroutes.http.request import Request
import pyroutes.settings as settings

class Dispatcher(object):

    def __init__(self):
        pass

    def create_middleware_chain(self, handler, request):
        chain = handler
        for full_path in settings.MIDDLEWARE:
            last_dot = full_path.rfind(".")
            module_name = full_path[:last_dot]
            class_name = full_path[last_dot + 1:]

            module = __import__(module_name, globals(), locals(), [class_name])
            middleware = getattr(module, class_name)

            chain = middleware(chain)

        return chain(request)

    def dispatch(self, environ, start_response):
        safe_data = threading.local()
        safe_data.request = Request(environ)

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
        complete_path = current_path
        handler = pyroutes.__request__handlers__.get(current_path, None)
        while handler is None and current_path:
            if current_path in pyroutes.__request__handlers__:
                handler = pyroutes.__request__handlers__[current_path]
                arg_count = len(complete_path.rstrip('/').split('/')) - len(current_path.rstrip('/').split('/'))
                if hasattr(handler, 'im_func'):
                    if handler.handler.im_func.func_code.co_argcount -2 != arg_count:
                        # Return the handler if even if the argument count from the url is wrong if we have defaults on everything
                        if len(handler.handler.im_func.func_defaults) + 1 == handler.handler.im_func.func_code.co_argcount:
                            return handler
                        return None
                elif handler.handler.func_code.co_argcount - 1 != arg_count:
                    # Return the handler if even if the argument count from the url is wrong if we have defaults on everything
                    if len(handler.handler.func_defaults) + 1 == handler.handler.func_code.co_argcount:
                        return handler
                    return None

            current_path = current_path[:current_path.rfind("/")]
        return handler
