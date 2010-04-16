from datetime import datetime
import os
import unittest
import wsgiref.util

from pyroutes.http.response import *
from pyroutes.http.request import Request
import pyroutes.settings as settings
import pyroutes.utils as utils

class TestDevServer(unittest.TestCase):

    def test_presence(self):
        utils.devserver

class TestFileServer(unittest.TestCase):
    def setUp(self):
        self.request_env = {}
        wsgiref.util.setup_testing_defaults(self.request_env)
        self.request = Request(self.request_env)

    def test_with_custom_settings(self):
        settings.DEV_MEDIA_BASE = '..'
        self.request.ENV['PATH_INFO'] = '/'
        response = utils.fileserver(self.request)
        self.assertNotEqual(response.content.find('<a href="pyroutes/">pyroutes/</a>'), -1)

    def test_if_modified_since(self):
        modified = datetime.fromtimestamp(os.path.getmtime('pyroutes'))
        modified = datetime.strftime(modified, "%a, %d %b %Y %H:%M:%S")
        self.request.ENV['PATH_INFO'] = '/pyroutes/'
        response = utils.fileserver(self.request)
        self.assertTrue(('Last-Modified', modified) in response.headers)
        self.request.ENV['HTTP_IF_MODIFIED_SINCE'] = modified
        response = utils.fileserver(self.request)
        self.assertEqual(response.status_code, '304 Not Modified')

    def test_no_upperlevel(self):
        self.request.ENV['PATH_INFO'] = '/pyroutes/../../'
        self.assertRaises(Http404, utils.fileserver, self.request)

    def test_redirects(self):
        self.request.ENV['PATH_INFO'] = '/pyroutes'
        response = utils.fileserver(self.request)
        self.assertEqual(response.status_code, '302 See Other')

    def test_listing(self):
        self.request.ENV['PATH_INFO'] = '/pyroutes/'
        response = utils.fileserver(self.request)
        self.assertEqual(response.status_code, '200 OK')
        for header in ['Content-Type', 'Last-Modified']:
            self.assertTrue(header in [a[0] for a in response.headers])
        self.assertNotEqual(response.content.find('<a href="__init__.py">__init__.py</a>'), -1)

    def test_host_file(self):
        self.request.ENV['PATH_INFO'] = '/tests/utils_test.py'
        response = utils.fileserver(self.request)
        self.assertEqual(response.status_code, '200 OK')
        for header in ['Last-Modified', 'Content-Length']:
            self.assertTrue(header in [a[0] for a in response.headers])
        self.assertTrue(('Content-Type', 'text/x-python') in response.headers)
        self.assertTrue(hasattr(response.content, 'filelike'))

    def test_noaccess(self):
        test_file = os.path.join('.', 'tests', 'responsetest.py')
        mode = os.stat(test_file).st_mode
        os.chmod(test_file, 0)
        try:
            self.request.ENV['PATH_INFO'] = '/tests/responsetest.py'
            self.assertRaises(Http403, utils.fileserver, self.request)
        finally:
            os.chmod(test_file, mode)

    def test_noaccess(self):
        self.request.ENV['PATH_INFO'] = '/404path/'
        self.assertRaises(Http404, utils.fileserver, self.request)
