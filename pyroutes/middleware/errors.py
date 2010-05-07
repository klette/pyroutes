import threading
import sys
import traceback

from pyroutes import settings
from pyroutes.http.response import Http404, Http500

class NotFoundMiddleware(object):
    def __init__(self, passthrough):
        self.d = threading.local()
        self.d.passthrough = passthrough

    def __call__(self, request):
        # If we got a handler, run it.
        if self.d.passthrough:
            return self.d.passthrough(request)

        error = Http404()
        return error.get_response(request.ENV['PATH_INFO'])


class ErrorHandlerMiddleware(object):
    def __init__(self, passthrough):
        self.d = threading.local()
        self.d.passthrough = passthrough
        self.d.response = None

    def __call__(self, request):
        try:
            self.d.response = self.d.passthrough(request)
        except Exception, exception:
            print exception
            error = Http500()
            if settings.DEBUG:
                exception_type, exception_value, exception_trace = sys.exc_info()
                trace = "".join(traceback.format_exception(exception_type,
                                                    exception_value,
                                                    exception_trace))
                self.d.response = error.get_response(
                        request.ENV['PATH_INFO'],
                        description="%s: %s" % (exception.__class__.__name__,
                                            exception),
                        traceback=trace)
            else:
                self.d.response = error.get_response(request.ENV['PATH_INFO'])
        
        return self.d.response

class HandlerDidNotReturnReponseObjectException(Exception):
    pass
