from os import path
import unittest

from pyroutes.http.response import *
import pyroutes.settings as settings

class TestResponse(unittest.TestCase):
    def test_empty_init(self):
        response = Response()
        self.assertEqual(response.content, [])
        self.assertEqual(response.headers, [('Content-Type', 'text/html; charset=utf-8')])
        self.assertEqual(response.status_code, '200 OK')

    def test_init(self):
        response = Response("Hello", [('Content-Length', 1000)], '500 Error')
        self.assertEqual(response.content, "Hello")
        self.assertEqual(response.headers, [('Content-Type', settings.DEFAULT_CONTENT_TYPE), ('Content-Length', 1000)])
        self.assertEqual(response.status_code, '500 Error')

class TestExceptions(unittest.TestCase):
    def test_base_exception(self):
        self.assertRaises(TypeError, HttpException)

    def _test_http_exception(self, exception, code, code_status):
        instance = exception()
        self.assertEqual(instance.code, code)
        response = instance.get_response('/foo')
        self.assertNotEqual(response.content.find(code_status), -1)
        self.assertEqual(response.headers, [('Content-Type', settings.DEFAULT_CONTENT_TYPE)])
        self.assertEqual(response.status_code, code_status)

    def _test_including_custom_templates(self, exception, code, code_status):
        # First, test with defalt settings
        self._test_http_exception(exception, code, code_status)
        base = settings.BUILTIN_TEMPLATES_DIR
        setattr(settings, 'TEMPLATE_%s' % code, settings.BUILTIN_BASE_TEMPLATE)
        # Then, with a template without inheritence
        self._test_http_exception(exception, code, code_status)
        setattr(settings, 'TEMPLATE_%s' % code, path.join(base, '%d.xml' % code))
        settings.CUSTOM_BASE_TEMPLATE = path.join(base, 'base.xml')
        # Finally, with templates with inheritance
        self._test_http_exception(exception, code, code_status)

    def test_403_exception(self):
        exception = Http403
        content = '403 Forbidden'
        self._test_including_custom_templates(exception, 403, content)

    def test_404_exception(self):
        exception = Http404
        content = '404 Not Found'
        self._test_including_custom_templates(exception, 404, content)

    def test_500_exception(self):
        exception = Http500
        content = '500 Server Error'
        self._test_including_custom_templates(exception, 500, content)

class TestRedirectResponse(unittest.TestCase):
    def test_init(self):
        redirect = Redirect('http://google.com')
        self.assertEqual(redirect.status_code, '302 See Other')
        self.assertEqual(redirect.headers, [('Location', "http://google.com")])
        self.assertEqual(redirect.content, 'redirect')


