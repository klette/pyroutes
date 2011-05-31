from pyroutes.http.response import Redirect

class AppendSlashes(object):
    """
    Used for adding slashes at the end of all URLs. i.e. GET /foo/bar will
    return a redirect to /foo/bar/
    """
    def __init__(self, passthrough, route):
        self.passthrough = passthrough

    def __call__(self, request):
        if not request.ENV['PATH_INFO'].endswith('/'):
            return Redirect(request.ENV['PATH_INFO'] + '/')
        return self.passthrough(request)
