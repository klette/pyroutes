import threading
import sys
import traceback

from pyroutes import settings
from pyroutes.http.response import Http404, Http500

class NotFoundMiddleware(object):
    def __init__(self, passthrough):
        self.d = threading.local()
        self.d.passthrough = passthrough

    def __call__(self, environ, start_response):
        # If we got a handler, run it.
        if self.d.passthrough:
            return self.d.passthrough(environ, start_response)

        error = Http404()
        response = error.get_response(environ['PATH_INFO'])

        start_response(response.status_code, response.headers)
        return [response.content]

class ErrorHandlerMiddleware(object):
    def __init__(self, passthrough):
        self.d = threading.local()
        self.d.passthrough = passthrough

    def __call__(self, environ, start_response):
        try:
            return self.d.passthrough(environ, start_response)
        except Exception, exception:
            error = Http500()
            if settings.DEBUG:
                exception_type, exception_value, exception_trace = sys.exc_info()
                trace = "".join(traceback.format_exception(exception_type,
                                                    exception_value,
                                                    exception_trace))
                response = error.get_response(
                        environ['PATH_INFO'],
                        description="%s: %s" % (exception.__class__.__name__,
                                            exception),
                        traceback=trace)
            else:
                response = error.get_response(environ['PATH_INFO'])
        
        start_response(response.status_code, response.headers)
        return [response.content]
