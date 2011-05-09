#!/usr/bin/env python
#encoding: utf-8

"""
Main pyroutes module

This module handles all the dispatching services for pyroutes.
"""

from pyroutes.route import Route
from pyroutes.dispatcher import Dispatcher

import logging

__routes__ = {}
dispatcher = Dispatcher()

logging.basicConfig()
logger = logging.getLogger('pyroutes')

def route(path):
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

    One property of the routes are that matches are done on an best effort
    basis, starting from the top of the tree and going down. This results in
    route being delt request for their defined path and any path under it
    matching the argument count of the function.
    """

    def decorator(func):
        """
        See the pyroutes.route docstring
        """
        if path in __routes__:
            logger.warn("Redefining handler for %s with %s" % \
                    (path, func))
        route_instance = Route(func, path)
        __routes__[path] = route_instance
        return route_instance
    return decorator

def reverse_url(handler_name, absolute_path=False):
    """
    Returns the path for a route.
    Example usage:
    >>> reverse_url('login')
    /account/login
    """
    for path, route in __routes__.items():
        if route.handler.__name__ == handler_name:
            if absolute_path:
                return path
            else:
                return '/'.join([settings.SITE_ROOT, path.strip('/')])
    raise ValueError('No handler function named %s' % handler_name)

def application(environ, start_response):
    """
    The application method, which is for use in a WSGI setup
    (Hint: this is how you set this up with any web server)
    Example usage:
    >>> from pyroutes import application

    See the documentation for more details.
    """
    return dispatcher.dispatch(environ, start_response)
