class Route(object):

    def __init__(self, handler, path):
        self.handler = handler
        self.path = path

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handler(request)

        headers = response.headers + response.cookies.cookie_headers
        start_response(response.status_code, headers)
        if isinstance(response.content, basestring):
            return [response.content]
        else:
            return response.content
