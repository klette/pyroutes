"""
Middleware for making non-response objects into Responses
"""

from pyroutes.http.response import Response

class Responsify(object):
    """
    If a non-response object s (e.g a string) is passed, returns Response(s)

    This allows e.g

        >>> @route('/')
        >>> def foo(request):
        >>>     return 'Hello, world!'

    or

        >>> bar = lambda x: 'Hello, lambda world!'
        >>> route('/')(bar)

    """
    def __init__(self, passthrough, route):
        self.passthrough = passthrough

    def __call__(self, request):
        response = self.passthrough(request)
        if not isinstance(response, Response):
            response = Response(response)
        return response
