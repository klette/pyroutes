"""
A module that holds the Route class. A Route is a mapping between a path (e.g.
/foo/) and a callable that is to be run when this path is accessed.
"""

import inspect

class Route(object):
    """
    The Route object. Noramlly created using the route function, not through
    direct initialization. Holds some meta for the mapping between URL and a
    function, and calls the inner handler function with the correct parameters
    when Route.__call__ is called.
    """

    def __init__(self, handler, path):
        self.handler = handler
        self.path = path
        self.maps = None

        args, varargs, varkw, defaults = inspect.getargspec(handler)
        self.arguments = args
        self.required_argument_length = len(args) - 1
        self.variable_arguments = varargs
        self.variable_defaults = defaults

    def __repr__(self):
        return u'Route(%s, %s)' % (self.handler.__name__, self.path)

    @property
    def __name__(self):
        return self.handler.__name__

    def __call__(self, request):
        return self.handler(request, *self.extract_url_params(request.ENV))

    def extract_url_params(self, environ):
        """
        Finds the parameters to pass to the route given the URL requested.
        """
        subpath = environ.get('PATH_INFO','')[len(self.path):]
        args = subpath.strip('/').split('/')
        if args[-1] == '':
            args.pop()
        return args
