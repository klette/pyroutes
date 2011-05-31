"""
A module containing a primitive timing middleware.
"""

import time

from pyroutes import settings

class TimingMiddleware(object):
    """
    This middleware add a timing number at the bottom of the page if
    settings.DEBUG is True if the response content type is
    text/html or application/xhtml+xml

    Primitive profiling, but quite useful.
    """
    def __init__(self, passthrough, route):
        self.passthrough = passthrough

    def __call__(self, request):
        if not settings.DEBUG:
            return self.passthrough(request)

        start_time = time.time()
        response = self.passthrough(request)
        end_time = time.time()
        for (header, value) in response.headers:
            if header == 'Content-Type':
                if (value.startswith('text/html') or
                        value.startswith('application/xhtml+xml')):
                    elapsed = (end_time - start_time) * 1000
                    if response.content.endswith('</html>'):
                        response.content = (response.content[:-len('</html>')] +
                                '<pre id="pyroutes_timing">Page took %0.3f' +
                                ' ms to generate</pre></html>' % elapsed)
                    else:
                        response.content += ('\n<pre id="pyroutes_timing">' +
                               'Page took %0.3f ms to generate</pre>' % elapsed)
        return response
