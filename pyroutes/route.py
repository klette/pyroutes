from pyroutes.http.request import Request

class Route(object):

    def __init__(self, handler, path):
        self.handler = handler
        self.path = path
        self.maps = None

    def __repr__(self):
        return u'Route(%s, %s)' % (self.handler.__name__, self.path)

    @property
    def __name__(self):
        return self.handler.__name__

    def __call__(self, request):
        return self.handler(request, *self.extract_url_params(request.ENV))

    def extract_url_params(self, environ):
        subpath = environ.get('PATH_INFO','')[len(self.path):]
        args = subpath.strip('/').split('/')
        if args == ['']:
            return []
        return args
