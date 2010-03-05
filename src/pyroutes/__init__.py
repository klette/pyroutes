#!/usr/bin/env python
#encoding: utf-8

"""
Main pyroutes module

This module handles all the dispatching services for pyroutes.
"""

from pyroutes.http.response import HttpException, Http404, Http500
from pyroutes.http.request import Request
from pyroutes import settings

from wsgiref.util import shift_path_info
import cgi
import os
import sys
import traceback

__request__handlers__ = {}

def route(path):
    """
    Decorates a function for handling page requests to
    a certain path
    """

    def decorator(func):
        """
        See the pyroutes.route-docstring
        """
        if path in __request__handlers__:
            raise ValueError("Tried to redefine handler for %s with %s" % \
                    (path, func))
        __request__handlers__[path] = func
    return decorator

def create_request_path(environ):
    """
    Returns a tuple consisting of the individual request parts
    """
    path = shift_path_info(environ)
    request = []
    if not path:
        request = ['/']
    else:
        while path:
            request.append(path)
            path = shift_path_info(environ)
    return request

def find_request_handler(current_path):
    """
    Locates the handler for the specified path. Return None if not found.
    """
    handler = None
    while handler is None:
        if current_path in __request__handlers__:
            handler = __request__handlers__[current_path]
            break
        current_path = current_path[:current_path.rfind("/")]
        if not current_path:
            return None
    return handler

def reverse_url(handler_name):
    """
    Returns the path for a handler.
    Example usage:
    >>> reverse_url('login')
    /account/login
    """
    for path, handler in __request__handlers__.items():
        if handler.__name__ == handler_name:
            return path
    raise ValueError('No handler named %s' % handler_name)

def application(environ, start_response):
    """
    Searches for a handler for a certain request and
    dispatches it if found. Returns 404 if not found.
    """

    request = create_request_path(environ.copy())
    complete_path = '/%s' % '/'.join(request)
    handler = find_request_handler(complete_path)
    if not handler:
        error = Http404()
        if settings.DEBUG:
            response = error.get_response(environ['PATH_INFO'],
                    details="Debug: No handler for path %s" % complete_path)
        else:
            response = error.get_response(environ['PATH_INFO'])
        start_response(response.status_code, response.headers)
        return [response.content]

    try:
        req = Request(environ)
        try:
            response = handler(req)
        except HttpException, exception:
            response = exception.get_response(environ['PATH_INFO'])
        headers = response.headers + response.cookies.cookie_headers
        start_response(response.status_code, headers)
        if isinstance(response.content, basestring):
            return [response.content]
        else:
            return response.content
    except Exception, exception:
        error = Http500()
        if settings.DEBUG:
            exception_type, exception_value, exception_trace = sys.exc_info()
            trace = "".join(traceback.format_exception(exception_type,
                                                    exception_value,
                                                    exception_trace))
            response = error.get_response(
                    environ['PATH_INFO'],
                    description="%s: %s" % (exception.__class__.__name__,
                                            exception),
                    traceback=trace)
        else:
            response = error.get_response(environ['PATH_INFO'])
        start_response(response.status_code, response.headers)
        return [response.content]
