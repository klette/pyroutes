# encoding: utf-8

import cgi
import simplejson
import unittest
import wsgiref.util

import pyroutes
from pyroutes.http.request import Request
from pyroutes.http.response import Response

import stderr_helper

class TestRoute(unittest.TestCase):
    def setUp(self):
        pyroutes.__routes__ = {}
        pyroutes.settings.DEBUG = True
        pyroutes.settings.SITE_ROOT = "/myapp"

        self.request_env = {}
        wsgiref.util.setup_testing_defaults(self.request_env)
        self.request = Request(self.request_env)

    def tearDown(self):
        reload(cgi)
        reload(pyroutes)

    def createAnonRoute(self, path):
        @pyroutes.route(path)
        def foo(bar, baz):
            pass
        return foo

    def testBasicRoute(self):
        self.createAnonRoute('/')
        self.assertTrue('/' in pyroutes.__routes__)
        self.assertTrue(len(pyroutes.__routes__) == 1)

    def testDoubleRouteException(self):
        self.createAnonRoute('/')
        try:
            stderr_helper.redirect_stderr()
            self.createAnonRoute('/')
            self.assertTrue(len(pyroutes.__routes__) == 1)
            self.assertTrue('Redefining' in stderr_helper.get_stderr_data())
        finally:
            stderr_helper.revert_stderr()

    def testReverseUrl(self):
        self.createAnonRoute('/')
        self.assertEquals(pyroutes.reverse_url('foo'), '/myapp/')

    def testReverseUrlNotFound(self):
        self.assertRaises(ValueError, pyroutes.reverse_url, 'bar')

    def testReverseUrlAbsolutePath(self):
        self.createAnonRoute("/path")
        self.assertEquals("/path", pyroutes.reverse_url("foo", absolute_path=True))

    def testReverseUrlRelativePath(self):
        self.createAnonRoute("/path")
        self.assertEquals("/myapp/path", pyroutes.reverse_url("foo"))
