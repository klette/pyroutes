import os
import unittest

import pyroutes.http as http
import pyroutes.settings as settings
import pyroutes.utils as utils

class TestDevServer(unittest.TestCase):
    def presence(self):
        # How the hell do we test this thing?
        self.assertTrue(hasattr(utils, 'devserver'))

class TestFileServer(unittest.TestCase):

    def test_with_custom_settings(self):
        # FIXME Teste with DEV_MEDIA_BASE set
        pass

    def test_if_modified_since(self):
        # FIXME Test for 304 Not Modified
        pass

    def test_redirects(self):
        response = utils.fileserver({'PATH_INFO': '/pyroutes'}, {})
        self.assertEqual(response.status_code, '302 See Other')

    def test_listing(self):
        response = utils.fileserver({'PATH_INFO': '/pyroutes/'}, {})
        self.assertEquals(response.status_code, '200 OK')
        for header in ['Content-Type', 'Last-Modified']:
            self.assertTrue(header in [a[0] for a in response.headers])
        self.assertNotEqual(response.content.find('<a href="__init__.py">__init__.py</a>'), -1)

    def test_host_file(self):
        response = utils.fileserver({'PATH_INFO': '/tests/utilstest.py'}, {})
        self.assertEquals(response.status_code, '200 OK')
        for header in ['Last-Modified', 'Content-Length']:
            self.assertTrue(header in [a[0] for a in response.headers])
        self.assertTrue(('Content-Type', 'text/x-python') in response.headers)
        self.assertTrue(hasattr(response.content, 'filelike'))

    def test_nonexistant(self):
        test_file = os.path.join('.', 'tests', 'httptest.py')
        mode = os.stat(test_file).st_mode
        os.chmod(test_file, 0)
        self.assertRaises(http.Http403, utils.fileserver, {'PATH_INFO': '/tests/httptest.py'}, {})
        os.chmod(test_file, mode)

    def test_noaccess(self):
        self.assertRaises(http.Http404, utils.fileserver, {'PATH_INFO': '/404path'}, {})
