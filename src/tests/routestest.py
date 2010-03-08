# encoding: utf-8

import unittest
import minimock
import cgi

from minimock import TraceTracker

import pyroutes


class TestRoute(unittest.TestCase):
    def setUp(self):
        pyroutes.__request__handlers__ = {}
        pyroutes.settings.DEBUG = True

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

