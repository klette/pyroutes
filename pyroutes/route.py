import threading

class Route(object):

    def __init__(self, handler, path):
        self.handler = handler
        self.path = path

    def __call__(self, environ, start_response):
        safe_data = threading.local()
        safe_data.request = Request(environ)
        safe_data.response = self.handler(request)

        safe_data.headers = safe_data.response.headers + safe_data.response.cookies.cookie_headers
        start_response(safe_data.response.status_code, safe_data.headers)
        if isinstance(safe_data.response.content, basestring):
            return [safe_data.response.content]
        else:
            return safe_data.response.content
