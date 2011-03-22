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
        return self.handler(request, **self.extract_url_params(request.ENV))

    def extract_url_params(self, environ):
        parts = environ.get('PATH_INFO','')[len(self.path)+1:].split('/')
        parameters = {}
        maps = None

        if len(self.handler.func_code.co_varnames) > 1:
            maps = self.handler.func_code.co_varnames[1:self.handler.func_code.co_argcount]
        
        defaults = self.handler.func_defaults or []

        if maps:
            parts.extend((len(maps)-len(parts)-len(defaults))*[None])
            for key, value in zip(maps, parts + list(defaults)):
                if key:
                    parameters[key] = value or ''
        return parameters
