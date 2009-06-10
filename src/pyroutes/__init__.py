#!/usr/bin/env python
#encoding: utf-8

from wsgiref.util import shift_path_info
import cgi
    
global __request__handlers__
__request__handlers__ = {}

def route(path):
    """
    Decorates a function for handling page requests to
    a certain path
    """
    global __request__handlers__
    
    def decorator(func):
        __request__handlers__[path] = func
    return decorator
    
def application(environ, start_response):
    """
    Searches for a handler for a certain request and
    dispatches it if found. Returns 404 if not found.
    """
    _environ = environ.copy()
    handlers = __request__handlers__.keys()
    path = shift_path_info(_environ)
    request = [] 
    if not path:
        request = ['/']
    else:
        while path:
            request.append(path)
            path = shift_path_info(_environ)

    handler = None
    complete_path = '/%s' % '/'.join(request)
    current_path = complete_path
    
    while handler is None:
        if current_path in handlers:
            handler = __request__handlers__[current_path]
            break
        current_path = current_path[:current_path.rfind("/")]
        if not current_path:
            start_response('404 Not Found', [('Content-type', 'text/plain')])
            return ["No handler found for path %s" % complete_path]
    try:
        _data = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=environ,
            keep_blank_values=False
        )
        data = {}
        for key in _data.keys():
            data[key] = _data.getvalue(key)
        response = handler(environ, data)
        start_response(response.status_code, response.headers)
        return[response.content]
    except Exception, exception:
        start_response('500 Error', [('Content-type', 'text/plain')])
        return ["An error occurred\n%s" % str(exception)]

    
