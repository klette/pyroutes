# encoding: utf-8

import unittest
import minimock
import cgi
import wsgiref.util

from minimock import TraceTracker

import pyroutes

from pyroutes.http.request import Request

class TestRoute(unittest.TestCase):
    def setUp(self):
        pyroutes.__request__handlers__ = {}
        pyroutes.settings.DEBUG = True

        self.request_env = {}
        wsgiref.util.setup_testing_defaults(self.request_env)
        self.request = Request(self.request_env)

    def tearDown(self):
        minimock.restore()
        reload(cgi)
        reload(pyroutes)

    def createAnonRoute(self, path):
        @pyroutes.route(path)
        def foo(bar, baz):
            pass
        return foo

    def testBasicRoute(self):
        self.createAnonRoute('/')
        self.assertTrue('/' in pyroutes.__request__handlers__)
        self.assertTrue(len(pyroutes.__request__handlers__) == 1)

    def testDoubleRouteException(self):
        self.createAnonRoute('/')
        self.assertRaises(ValueError, self.createAnonRoute, '/')
        self.assertTrue(len(pyroutes.__request__handlers__) == 1)


    def testCreateRequestPath(self):
        self.assertEquals(['foo', 'bar'], pyroutes.create_request_path({'PATH_INFO': '/foo/bar'}))
        self.assertEquals(['foo', 'bar'], pyroutes.create_request_path({'PATH_INFO': '/foo/bar/'}))
        self.assertEquals(['/'], pyroutes.create_request_path({'PATH_INFO': '/'}))
        self.assertEquals(['/'], pyroutes.create_request_path({'PATH_INFO': '//'}))

    def testFindRequestHandler(self):
        self.createAnonRoute('/')
        self.createAnonRoute('/bar')
        self.assertTrue(pyroutes.find_request_handler('/') != None)
        self.assertTrue(pyroutes.find_request_handler('/bar') != None)
        self.assertTrue(pyroutes.find_request_handler('/baz') == None)

    def testReverseUrl(self):
        self.createAnonRoute('/')
        self.assertEquals(pyroutes.reverse_url('foo'), '/')

    def testReverseUrlNotFound(self):
        self.assertRaises(ValueError, pyroutes.reverse_url, 'bar')

