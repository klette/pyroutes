# encoding: utf-8

import cgi
import simplejson
import unittest
import wsgiref.util

import pyroutes
from pyroutes.http.request import Request
from pyroutes.http.response import Response

class TestRoute(unittest.TestCase):
    def setUp(self):
        pyroutes.__request__handlers__ = {}
        pyroutes.settings.DEBUG = True

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
        self.assertTrue('/' in pyroutes.__request__handlers__)
        self.assertTrue(len(pyroutes.__request__handlers__) == 1)

    def testDoubleRouteException(self):
        self.createAnonRoute('/')
        self.assertRaises(ValueError, self.createAnonRoute, '/')
        self.assertTrue(len(pyroutes.__request__handlers__) == 1)


    def testReverseUrl(self):
        self.createAnonRoute('/')
        self.assertEquals(pyroutes.reverse_url('foo'), '/')

    def testReverseUrlNotFound(self):
        self.assertRaises(ValueError, pyroutes.reverse_url, 'bar')

    def testUrlParameters(self):
        #TODO: Make this test prettier.
        @pyroutes.route('/archive')
        def archive(request, year, month, day):
            return Response(";".join((year, month, day)))
        self.request_env['PATH_INFO'] = '/archive/2010/01/02'
        def foo(x,y):
            pass
        req = "".join(pyroutes.application(self.request_env, foo))
        params = req.split(";")
        self.assertEquals(params[0], '2010')
        self.assertEquals(params[1], '01')
        self.assertEquals(params[2], '02')

    def testUrlParametersTooManyParams(self):
        #TODO: Make this test prettier.
        @pyroutes.route('/archive')
        def archive(request, year, month, day):
            return Response(";".join((year, month, day)))
        self.request_env['PATH_INFO'] = '/archive/2010/01/02/atom'
        def foo(x,y):
            pass
        req = "".join(pyroutes.application(self.request_env, foo))
        params = req.split(";")
        self.assertEquals(params[0], '2010')
        self.assertEquals(params[1], '01')
        self.assertEquals(params[2], '02')

    def testUrlParametersTooFewParams(self):
        #TODO: Make this test prettier.
        @pyroutes.route('/archive')
        def archive(request, year, month, day):
            return Response(";".join((year, month, day)))
        self.request_env['PATH_INFO'] = '/archive/2010/01'
        def foo(x,y):
            pass
        req = "".join(pyroutes.application(self.request_env, foo))
        params = req.split(";")
        self.assertEquals(params[0], '2010')
        self.assertEquals(params[1], '01')
        self.assertEquals(params[2], '')

