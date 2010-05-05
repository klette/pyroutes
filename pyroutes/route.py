import threading
from pyroutes.http.request import Request

class Route(object):

    def __init__(self, handler, path):
        self.handler = handler
        self.path = path
        self.maps = None

        if len(handler.func_code.co_varnames) > 1:
            self.maps = \
                handler.func_code.co_varnames[1:handler.func_code.co_argcount]

    def __repr__(self):
        return u'Route(%s, %s)' % (self.handler.__name__, self.path)

    @property
    def __name__(self):
        return self.handler.__name__

    def __call__(self, request):
        return self.handler(request, **self.extract_url_params(request.ENV))

    def extract_url_params(self, environ):
        parts = environ.get('PATH_INFO','')[len(self.path)+1:].split('/')
        parameters = {}
        if self.maps:
            parts.extend((len(self.maps)-len(parts)-len(self.handler.func_defaults or []))*[None])
            for key, value in zip(self.maps, parts + list(self.handler.func_defaults or [])):
                if key:
                    parameters[key] = value or ''

        return parameters
