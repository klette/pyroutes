import threading
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
        # Check if handler is a class based route
        if hasattr(self.handler, 'im_self'):
            localstore = threading.local()
            localstore.handler_class_instance = self.handler.im_class()
            localstore.handler = getattr(localstore.handler_class_instance, self.handler.__name__)
            return localstore.handler(request, **self.extract_url_params(localstore.handler, request.ENV))
        else:
            return self.handler(request, **self.extract_url_params(self.handler, request.ENV))

    def extract_url_params(self, handler, environ):
        parts = environ.get('PATH_INFO','')[len(self.path)+1:].split('/')
        parameters = {}
        maps = None

        if hasattr(handler, 'im_func'):
            if len(handler.im_func.func_code.co_varnames) > 2:
                maps = handler.im_func.func_code.co_varnames[2:handler.im_func.func_code.co_argcount]
            defaults = handler.im_func.func_defaults
        else:
            if len(handler.func_code.co_varnames) > 1:
                maps = handler.func_code.co_varnames[1:handler.func_code.co_argcount]
            defaults = handler.func_defaults

        if maps:
            parts.extend((len(maps)-len(parts)-len(defaults or []))*[None])
            for key, value in zip(maps, parts + list(defaults or [])):
                if key:
                    parameters[key] = value or ''
        return parameters
