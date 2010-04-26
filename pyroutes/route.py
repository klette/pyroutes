import threading
from pyroutes.http.request import Request

class Route(object):

    def __init__(self, handler, path):
        self.handler = handler
        self.path = path
        self.maps = None

        if len(handler.func_code.co_varnames) > 1:
            self.maps = handler.func_code.co_varnames[1:]

    def __repr__(self):
        return u'Route(%s, %s)' % (self.handler.__name__, self.path)

    @property
    def __name__(self):
        return self.handler.__name__

    def __call__(self, environ, start_response):
        safe_data = threading.local()
        safe_data.request = Request(environ)
        safe_data.response = self.handler(safe_data.request, **self.extract_url_params(environ))
        safe_data.headers = safe_data.response.headers + safe_data.response.cookies.cookie_headers
        start_response(safe_data.response.status_code, safe_data.headers)
        if isinstance(safe_data.response.content, basestring):
            return [safe_data.response.content]
        else:
            return safe_data.response.content

    def extract_url_params(self, environ):
        parts = environ.get('PATH_INFO','')[len(self.path)+1:].split('/')
        return dict(((k,v or '') for k,v in map(None, *[self.maps, parts]) if k))
