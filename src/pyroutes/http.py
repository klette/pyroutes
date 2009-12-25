#!/usr/bin/env python
# encoding: utf-8
"""
http.py

A collection of Response classes for pyroutes
"""

class Response:
    """
    A wrapper class for a response to a route. Takes
    a content, headers and status_code parameter.
    headers should be passed in as a tuple.
    """
    def __init__(self, content=None, headers=None, status_code='200 OK'):
        if content is None:
            self.content = []
        else:
            self.content = content
        if headers is None:
            self.headers = [('Content-Type', 'text/html; charset=utf8')]
        else:
            self.headers = headers
        self.status_code = status_code


class Redirect(Response):
    """
    A redirect shortcut class for redirection responses
    """

    def __init__(self, location):
        self.content = "redirect"
        self.headers = [('Location', location)]
        self.status_code = "302 See Other"


