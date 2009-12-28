import unittest

import pyroutes.http as http
import pyroutes.settings as settings

class TestResponse(unittest.TestCase):
    def test_empty_init(self):
        response = http.Response()
        self.assertEqual(response.content, [])
        self.assertEqual(response.headers, [('Content-Type', 'text/html; charset=utf-8')])
        self.assertEqual(response.status_code, '200 OK')

    def test_init(self):
        response = http.Response("Hello", [('Content-Length', 1000)], '500 Error')
        self.assertEqual(response.content, "Hello")
        self.assertEqual(response.headers, [('Content-Type', settings.DEFAULT_CONTENT_TYPE), ('Content-Length', 1000)])
        self.assertEqual(response.status_code, '500 Error')

class TestRedirectResponse(unittest.TestCase):
    def test_init(self):
        redirect = http.Redirect('http://google.com')
        self.assertEqual(redirect.status_code, '302 See Other')
        self.assertEqual(redirect.headers, [('Location', "http://google.com")])
        self.assertEqual(redirect.content, 'redirect')
