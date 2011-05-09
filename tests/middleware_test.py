import unittest
from pyroutes.middleware.errors import *
from pyroutes.http.response import *
from pyroutes.http.request import Request
import pyroutes.settings
import wsgiref.util
import stderr_helper

def passtrough(req):
    return True

class TestNotFoundMiddleware(unittest.TestCase):

    def setUp(self):
        self.request_env = {}
        wsgiref.util.setup_testing_defaults(self.request_env)
        self.request = Request(self.request_env)

    def test_should_call_handler_if_found(self):
        nfm = NotFoundMiddleware(passtrough)
        self.assertTrue(nfm(self.request))

    def test_should_return_404_if_no_handler(self):
        nfm = NotFoundMiddleware(None)
        self.assertEquals(nfm(self.request).status_code, '404 Not Found')


class TestErrorHandlerMiddleware(unittest.TestCase):

    def setUp(self):
        self.request_env = {}
        wsgiref.util.setup_testing_defaults(self.request_env)
        self.request = Request(self.request_env)

    def test_should_return_handler_result_if_no_exception(self):
        ehm = ErrorHandlerMiddleware(passtrough)
        self.assertTrue(isinstance(ehm(self.request), bool))

    def test_should_return_500_and_print_to_stderr_if_exception(self):
        def errorous(req):
            raise ValueError("foobar")
        try:
            stderr_helper.redirect_stderr()
            ehm = ErrorHandlerMiddleware(errorous)
            self.assertEquals(ehm(self.request).status_code, '500 Internal Server Error')
            self.assertTrue('ValueError' in stderr_helper.get_stderr_data())
        finally:
            stderr_helper.revert_stderr()

    def test_debug_honored(self):
        old_debug = pyroutes.settings.DEBUG
        pyroutes.settings.DEBUG = True
        def errorous(req):
            raise ValueError("foobar")
        ehm = ErrorHandlerMiddleware(errorous)
        response = ehm(self.request)
        self.assertEquals(response.status_code, '500 Internal Server Error')
        self.assertTrue('ValueError' in response.content)
        pyroutes.settings.DEBUG = old_debug

    def test_return_403(self):
        def errorous(req):
            raise Http403
        ehm = ErrorHandlerMiddleware(errorous)
        self.assertEquals(ehm(self.request).status_code, '403 Forbidden')

    def test_return_404(self):
        def errorous(req):
            raise Http404
        ehm = ErrorHandlerMiddleware(errorous)
        self.assertEquals(ehm(self.request).status_code, '404 Not Found')
