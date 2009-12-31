#!/usr/bin/env python
# encoding: utf-8
"""
http.py

A collection of Response classes for pyroutes
"""

from pyroutes.template import TemplateRenderer
from pyroutes import settings
import os
import hmac
import base64

try:
    from hashlib import sha1
except ImportError:
    import sha as sha1

class Response(object):
    """
    A wrapper class for a response to a route. Takes
    a content, headers and status_code parameter.
    headers should be passed in as a list of tuples.
    If default_content_header is set and no Content-Type header is set,
    settings.DEFAULT_CONTENT_TYPE is added as Content-Type.
    """
    def __init__(self, content=None, headers=None, status_code='200 OK',
            default_content_header=True):
        if content is None:
            self.content = []
        else:
            self.content = content

        self.headers = []
        if default_content_header:
            # We can do this regardless of if the header is set in headers.
            # That's because the last header definition takes precedense.
            self.headers.append(('Content-Type', settings.DEFAULT_CONTENT_TYPE))
        if not headers is None:
            self.headers += headers
        self.status_code = status_code

    def add_cookie(self, key, value):
        key = base64.b64encode(key)
        value = base64.b64encode(value)
        hash = hmac.HMAC(settings.SECRET_KEY, key + value, sha1).hexdigest()
        self.headers.append(('Set-Cookie', '%s=%s' % (key, value)))
        self.headers.append(('Set-Cookie', '%s_hash=%s' % (key, hash)))

    def del_cookie(self, key):
        key = base64.b64encode(key)
        self.headers.append(('Set-Cookie', "%s=null; expires=Thu, 01-Jan-1970 00:00:01 GMT" % key))
        self.headers.append(('Set-Cookie', "%s_hash=null; expires=Thu, 01-Jan-1970 00:00:01 GMT" % key))


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
            raise TypeError('You tried to instanciate HttpException. ' \
                    + 'Please, only create instances of Http{403,404,500}.')

        self.template_variable = 'TEMPLATE_%d' % self.code
        self.template_filename = '%d.xml' % self.code
        self.status_code = {
            403: '403 Forbidden',
            404: '404 Not Found',
            500: '500 Server Error'
        }[self.code]

        if hasattr(settings, self.template_variable):
            if hasattr(settings, 'CUSTOM_BASE_TEMPLATE'):
                self.templaterenderer = TemplateRenderer(
                    settings.CUSTOM_BASE_TEMPLATE
                )
            else:
                self.templaterenderer = TemplateRenderer()
            self.template = getattr(settings, self.template_variable)
        else:
            self.templaterenderer = TemplateRenderer(
                settings.BUILTIN_BASE_TEMPLATE
            )
            self.template = os.path.join(
                settings.BUILTIN_TEMPLATES_DIR,
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
