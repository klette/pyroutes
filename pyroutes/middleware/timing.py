from pyroutes import settings
import time
import threading

class TimingMiddleware(object):
    """
    This middleware add a timing number at the bottom of the page if
    settings.DEBUG is True if the response content type is
    text/html or application/xhtml+xml

    Primitive profiling, but quite useful.
    """
    def __init__(self, passthrough):
        self.d = threading.local()
        self.d.passthrough = passthrough

    def __call__(self, request):
        if not settings.DEBUG:
            return self.d.passthrough(request)

        self.d.start_time = time.time()
        response = self.d.passthrough(request)
        self.d.end_time = time.time()
        for (header, value) in response.headers:
            if header == 'Content-Type':
                if value.startswith('text/html') or \
                  value.startswith('application/xhtml+xml'):
                    elapsed = (self.d.end_time - self.d.start_time) * 1000
                    if response.content.endswith('</html>'):
                        response.content = response.content[:-len('</html>')] + \
                        '<pre>Page took %0.3f ms to generate</pre></html>' % elapsed
                    else:
                        response.content += '\n<pre>Page took %0.3f ms to generate</pre>' % elapsed
        return response
