from datetime import datetime
import os
import unittest

from pyroutes.http.response import *
import pyroutes.settings as settings
import pyroutes.utils as utils

class TestDevServer(unittest.TestCase):

    def test_presence(self):
        utils.devserver

class TestFileServer(unittest.TestCase):

    def test_with_custom_settings(self):
        settings.DEV_MEDIA_BASE = '..'
        response = utils.fileserver({'PATH_INFO': '/src/'}, {})
        self.assertNotEqual(response.content.find('<a href="pyroutes/">pyroutes/</a>'), -1)

    def test_if_modified_since(self):
        modified = datetime.fromtimestamp(os.path.getmtime('pyroutes'))
        modified = datetime.strftime(modified, "%a, %d %b %Y %H:%M:%S")
        response = utils.fileserver({'PATH_INFO': '/pyroutes/'}, {})
        self.assertTrue(('Last-Modified', modified) in response.headers)
        response = utils.fileserver({'PATH_INFO': '/pyroutes/', 'HTTP_IF_MODIFIED_SINCE': modified}, {})
        self.assertEqual(response.status_code, '304 Not Modified')

    def test_no_upperlevel(self):
        self.assertRaises(Http404, utils.fileserver, {'PATH_INFO': '/pyroutes/../../'}, {})

    def test_redirects(self):
        response = utils.fileserver({'PATH_INFO': '/pyroutes'}, {})
        self.assertEqual(response.status_code, '302 See Other')

    def test_listing(self):
        response = utils.fileserver({'PATH_INFO': '/pyroutes/'}, {})
        self.assertEqual(response.status_code, '200 OK')
        for header in ['Content-Type', 'Last-Modified']:
            self.assertTrue(header in [a[0] for a in response.headers])
        self.assertNotEqual(response.content.find('<a href="__init__.py">__init__.py</a>'), -1)

    def test_host_file(self):
        response = utils.fileserver({'PATH_INFO': '/tests/utilstest.py'}, {})
        self.assertEqual(response.status_code, '200 OK')
        for header in ['Last-Modified', 'Content-Length']:
            self.assertTrue(header in [a[0] for a in response.headers])
        self.assertTrue(('Content-Type', 'text/x-python') in response.headers)
        self.assertTrue(hasattr(response.content, 'filelike'))

    def test_nonexistant(self):
        test_file = os.path.join('.', 'tests', 'responsetest.py')
        mode = os.stat(test_file).st_mode
        os.chmod(test_file, 0)
        self.assertRaises(Http403, utils.fileserver, {'PATH_INFO': '/tests/httptest.py'}, {})
        os.chmod(test_file, mode)

    def test_noaccess(self):
        self.assertRaises(Http404, utils.fileserver, {'PATH_INFO': '/404path'}, {})
