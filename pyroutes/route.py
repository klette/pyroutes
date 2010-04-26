import threading
from pyroutes.http.request import Request

class Route(object):

    def __init__(self, handler, path, *args, **kwargs):
        self.handler = handler
        self.path = path
        self.maps = args

    def __repr__(self):
        return u'Route(%s, %s)' % (self.handler.__name__, self.path)

    @property
    def __name__(self):
        return self.handler.__name__

    def __call__(self, environ, start_response):
        safe_data = threading.local()
        safe_data.request = Request(environ)
        safe_data.response = self.handler(safe_data.request)

        safe_data.headers = safe_data.response.headers + safe_data.response.cookies.cookie_headers
        start_response(safe_data.response.status_code, safe_data.headers)
        if isinstance(safe_data.response.content, basestring):
            return [safe_data.response.content]
        else:
            return safe_data.response.content
