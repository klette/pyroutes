import unittest
from pyroutes.middleware.errors import *
from pyroutes.middleware.appendslash import AppendSlashes
from pyroutes.middleware.responsify import Responsify
from pyroutes.http.response import *
from pyroutes.http.request import Request
import pyroutes.settings
import wsgiref.util
import stderr_helper

def passtrough(req):
    return 'PASSTHROUGH'

def route(req):
    return 'ROUTE'

def redirect(req):
    return Redirect('/')

class TestNotFoundMiddleware(unittest.TestCase):

    def setUp(self):
        self.request_env = {}
        wsgiref.util.setup_testing_defaults(self.request_env)
        self.request = Request(self.request_env)

    def test_should_call_handler_if_found(self):
        nfm = NotFoundMiddleware(passtrough, route)
        self.assertTrue(nfm(self.request))

    def test_should_return_404_if_no_handler(self):
        nfm = NotFoundMiddleware(passtrough, None)
        self.assertEquals(nfm(self.request).status_code, '404 Not Found')


class TestErrorHandlerMiddleware(unittest.TestCase):

    def setUp(self):
        self.request_env = {}
        wsgiref.util.setup_testing_defaults(self.request_env)
        self.request = Request(self.request_env)

    def test_should_return_handler_result_if_no_exception(self):
        ehm = ErrorHandlerMiddleware(passtrough, route)
        self.assertEquals(ehm(self.request), 'PASSTHROUGH')

    def test_should_return_500_and_print_to_stderr_if_exception(self):
        def errorous(req):
            raise ValueError("foobar")
        try:
            stderr_helper.redirect_stderr()
            ehm = ErrorHandlerMiddleware(errorous, route)
            self.assertEquals(ehm(self.request).status_code, '500 Internal Server Error')
            self.assertTrue('ValueError' in stderr_helper.get_stderr_data())
        finally:
            stderr_helper.revert_stderr()

    def test_debug_honored(self):
        old_debug = pyroutes.settings.DEBUG
        pyroutes.settings.DEBUG = True
        def errorous(req):
            raise ValueError("foobar")
        ehm = ErrorHandlerMiddleware(errorous, route)
        response = ehm(self.request)
        self.assertEquals(response.status_code, '500 Internal Server Error')
        self.assertTrue('ValueError' in response.content)
        pyroutes.settings.DEBUG = old_debug

    def test_return_403(self):
        def errorous(req):
            raise Http403
        ehm = ErrorHandlerMiddleware(errorous, route)
        self.assertEquals(ehm(self.request).status_code, '403 Forbidden')

    def test_return_404(self):
        def errorous(req):
            raise Http404
        ehm = ErrorHandlerMiddleware(errorous, route)
        self.assertEquals(ehm(self.request).status_code, '404 Not Found')

class TestResponsifyMiddleware(unittest.TestCase):

    def test_should_return_response_subclass(self):
        respmw = Responsify(redirect, route)
        request = Request({})
        response = respmw(request)
        self.assertEquals(response.__class__, Redirect)

    def test_should_return_response(self):
        respmw = Responsify(passtrough, route)
        request = Request({})
        response = respmw(request)
        self.assertEquals(response.__class__, Response)
        self.assertEquals(response.content, 'PASSTHROUGH')

class TestAppendSlashMiddleware(unittest.TestCase):

    def setUp(self):
        self.asm = AppendSlashes(passtrough, route)
        pyroutes.settings.SITE_ROOT = ''

    def test_should_return_redirect_on_missing_slash(self):
        request = Request({'PATH_INFO': '/foo', 'QUERY_STRING': ''})
        request.matched_path = '/foo'
        response = self.asm(request)
        self.assertEquals(response.__class__, Redirect)

    def test_should_return_passthrough_on_slash(self):
        request = Request({'PATH_INFO': '/foo/'})
        response = self.asm(request)
        self.assertEquals(response, 'PASSTHROUGH')
