from pyroutes.http.response import Redirect

def AppendSlashes(passthrough, route):
    """
    Used for adding slashes at the end of all URLs. i.e. GET /foo/bar will
    return a redirect to /foo/bar/
    """
    def appendslash(request):
        if not request.ENV['PATH_INFO'].endswith('/'):
            return Redirect(request.ENV['PATH_INFO'] + '/')
        return passthrough(request)
    return appendslash
