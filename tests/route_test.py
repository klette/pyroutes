"""
Testing of the Route-class
"""

import unittest
from pyroutes.route import Route
from pyroutes import *
from pyroutes.http.request import Request

def _pass(request, bar, baz):
    pass

class RouteTest(unittest.TestCase):

    def testInit(self):
        route = Route(_pass, '/foo')
        self.assertEquals(route.handler, _pass)
        self.assertEquals(route.path, '/foo')

    def testRepr(self):
        route = Route(_pass, '/foo')
        self.assertEquals(repr(route), u'Route(_pass, /foo)')

    def testName(self):
        route = Route(_pass, '/foo')
        self.assertEquals(_pass.__name__, route.__name__)

    def testCall(self):
        env = {'PATH_INFO': '/foo/foo/faz'}
        route = Route(_pass, '/foo')
        self.assertEquals(route(Request(env)), None)

    def testExtractUrlParams(self):
        route = Route(_pass, '/foo')
        env = {'PATH_INFO': '/foo/foo/faz'}
        def test(req, bar, baz):
            pass
        self.assertEquals(route.extract_url_params(env), ['foo', 'faz'])

        route_instance = Route(_pass, '/')
        env = {'PATH_INFO': '/foo/foo'}
        self.assertEquals(route_instance.extract_url_params(env), ['foo', 'foo'])


        route_instance = Route(_pass, '/xim')
        env = {'PATH_INFO': '/xim/foo/bar'}
        self.assertEquals(route.extract_url_params(env), ['foo', 'bar'])
