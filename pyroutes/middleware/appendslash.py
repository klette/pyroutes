from pyroutes.http.response import Redirect
from pyroutes import LOGGER

class AppendSlashes(object):
    """
    Used for adding slashes at the end of all URLs. i.e. GET /foo/bar will
    return a redirect to /foo/bar/
    """
    def __init__(self, passthrough, route):
        self.passthrough = passthrough

    def __call__(self, request):
        if request.ENV['PATH_INFO'] != request.matched_path:
            return self.passthrough(request)
        if request.ENV['QUERY_STRING'] or request.POST:
            LOGGER.warn('Redirect issued using AppendSlashes middleware,' +
                    ' and data was submitted to the path.')
            if request.POST:
                return self.passthrough(request)
            return Redirect(request.ENV['PATH_INFO'] + '/?' +
                    request.ENV['QUERY_STRING'])
        if request.ENV['PATH_INFO'].endswith('/'):
            return self.passthrough(request)
        return Redirect(request.ENV['PATH_INFO'] + '/')
