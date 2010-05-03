#!/usr/bin/env python
#encoding: utf-8

"""
Main pyroutes module

This module handles all the dispatching services for pyroutes.
"""

from pyroutes.route import Route
from pyroutes.middleware.errors import *
import pyroutes.settings as settings

from wsgiref.util import shift_path_info

__request__handlers__ = {}

def route(path, *args, **kwargs):
    """
    Routes define which methods handles requests to certain paths, and are defined
    using the `@route`-decorator. The decorator takes one argument that defines which
    path the method is used for. The decorated function recieves one argument from pyroutes
    containing a `Request`-instance with all the information for that particular request.

    **Defining routes**

    This is a simple example route ::

      from pyroutes import route
      from pyroutes.http.response import Response

      @route('/')
      def index(request):
          return Response('Hello world')


    **How routes are matched to paths.**

    One property of the routes are that matches are done on an best effort basis, starting
    from the top of the tree and going down. This results in handler being delt request for
    their defined path and every path over it. This is true for all paths except the
    root-handler ('/').
    """

    def decorator(func):
        """
        See the pyroutes.route-docstring
        """
        if path in __request__handlers__:
            raise ValueError("Tried to redefine handler for %s with %s" % \
                    (path, func))
        route_instance = Route(func, path, *args, **kwargs)
        __request__handlers__[path] = route_instance
        return route_instance
    return decorator

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

    handler = find_request_handler(environ['PATH_INFO'])

    return ErrorHandlerMiddleware(NotFoundMiddleware(handler))(environ, start_response)
