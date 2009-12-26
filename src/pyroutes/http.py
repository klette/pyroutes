#!/usr/bin/env python
# encoding: utf-8
"""
http.py

A collection of Response classes for pyroutes
"""

from pyroutes.template import TemplateRenderer
import pyroutes
import os

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

class HttpException(Exception):
    def __init__(self):
        if not hasattr(self, 'code'):
            raise Exception('You tried to create an HttpException instance. ' \
                    + 'Please, only create instances of Http{403,404,500}.')

        self.template_variable = '%d_TEMPLATE' % self.code
        self.template_filename = '%d.xml' % self.code
        self.status_code = {
            403: '403 Forbidden',
            404: '404 Not Found',
            500: '500 Server Error'
        }[self.code]

        if hasattr(pyroutes.settings, self.template_variable):
            if hasattr(pyroutes.settings, CUSTOM_BASE_TEMPLATE):
                self.templaterenderer = TemplateRenderer(
                    pyroutes.settings.CUSTOM_BASE_TEMPLATE
                )
            else:
                self.templaterenderer = TemplateRenderer()
            self.template = getattr(pyroutes.settings, self.template_variable)
        else:
            self.templaterenderer = TemplateRenderer(
                pyroutes.settings.BUILTIN_BASE_TEMPLATE
            )
            self.template = os.path.join(
                pyroutes.settings.BUILTIN_TEMPLATES_DIR,
                self.template_filename
            )

    def get_response(self, path, **kwargs):
        template_data = {
            'request': path,
            'title': self.status_code
        }
        template_data.update(kwargs)
        document = self.templaterenderer.render(self.template, template_data)
        return Response(document, status_code=self.status_code)

class Http403(HttpException):
    code = 403

class Http404(HttpException):
    code = 404

class Http500(HttpException):
    code = 500
