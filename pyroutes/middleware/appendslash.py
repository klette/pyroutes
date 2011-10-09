"""
Contains the AppendSlashes middleware.
"""

from pyroutes.http.response import Redirect
from pyroutes import LOGGER

class AppendSlashes(object):
    """
    The Appendslashes middleware will redirect requests that are obviously
    missing a slash. If you request the path /foo, and there exists a route for
    /foo/, you are redirected to /foo/.
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
