import unittest
from pyroutes.middleware.errors import *
from pyroutes.http.response import *
from pyroutes.http.request import Request
import wsgiref.util
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

    def test_should_return_500_if_exception(self):
        def errorous(req):
            raise ValueError("foobar")

        ehm = ErrorHandlerMiddleware(errorous)
        self.assertEquals(ehm(self.request).status_code, '500 Internal Server Error')
