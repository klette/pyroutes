import sys
import traceback

from pyroutes import settings
from pyroutes.http.response import Http404, Http500

class NotFoundMiddleware(object):
    def __init__(self, passthrough):
        self.passthrough = passthrough

    def __call__(self, request):
        # If we got a handler, run it.
        if self.passthrough:
            return self.passthrough(request)

        error = Http404()
        return error.get_response(request.ENV['PATH_INFO'])


class ErrorHandlerMiddleware(object):
    def __init__(self, passthrough):
        self.passthrough = passthrough
        self.response = None

    def __call__(self, request):
        try:
            self.response = self.passthrough(request)
        except Exception, exception:
            error = Http500()
            if settings.DEBUG:
                exception_type, exception_value, exception_trace = sys.exc_info()
                trace = "".join(traceback.format_exception(exception_type,
                                                    exception_value,
                                                    exception_trace))
                self.response = error.get_response(
                        request.ENV['PATH_INFO'],
                        description="%s: %s" % (exception.__class__.__name__,
                                            exception),
                        traceback=trace)
            else:
                self.response = error.get_response(request.ENV['PATH_INFO'])
        
        return self.response

class HandlerDidNotReturnReponseObjectException(Exception):
    pass
