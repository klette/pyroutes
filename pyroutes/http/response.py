#!/usr/bin/env python
# encoding: utf-8
"""
response.py

A collection of Response classes for pyroutes
"""

from pyroutes.template import TemplateRenderer
from pyroutes.http.cookies import ResponseCookieHandler
from pyroutes import settings

try:
    from httplib import responses
except ImportError:
    responses = {
        100: 'Continue',
        101: 'Switching Protocols',
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'Non-Authoritative Information',
        204: 'No Content',
        205: 'Reset Content',
        206: 'Partial Content',
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Found',
        303: 'See Other',
        304: 'Not Modified',
        305: 'Use Proxy',
        306: '(Unused)',
        307: 'Temporary Redirect',
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed',
        413: 'Request Entity Too Large',
        414: 'Request-URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Requested Range Not Satisfiable',
        417: 'Expectation Failed',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported'}

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

        header_names = []
        if headers:
            header_names = map(lambda h: h[0], headers)

        self.headers = []
        if default_content_header and 'Content-Type' not in header_names:
            # Whether or not this is a safe operation may be python/wsgiref
            # version dependent. TODO: Should be tested and documented.
            self.headers.append(('Content-Type', settings.DEFAULT_CONTENT_TYPE))
        if not headers is None:
            self.headers += headers

        if status_code in responses:
            self.status_code = "%s %s" % (status_code, responses[status_code])
        else:
            self.status_code = status_code

        self.cookies = ResponseCookieHandler()

class Redirect(Response):
    """
    A redirect shortcut class for redirection responses
    """

    def __init__(self, location):
        self.content = "redirect"
        self.headers = [('Location', location)]
        self.status_code = "302 See Other"
        self.cookies = ResponseCookieHandler()

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
                settings.BUILTIN_BASE_TEMPLATE,
                template_dir=settings.BUILTIN_TEMPLATES_DIR
            )
            self.template = self.template_filename

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
