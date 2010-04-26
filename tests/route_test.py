"""
Testing of the Route-class
"""

import unittest
from pyroutes.route import Route

def _pass(foo):
    pass

class RouteTest(unittest.TestCase):

    def testInit(self):
        route = Route(_pass, '/foo', 'bar','baz')
        self.assertEquals(route.handler, _pass)
        self.assertEquals(route.path, '/foo')
        self.assertEquals(route.maps, ('bar', 'baz'))

    def testRepr(self):
        route = Route(_pass, '/foo', 'bar','baz')
        self.assertEquals(repr(route), u'Route(_pass, /foo)')

    def testName(self):
        route = Route(_pass, '/foo', 'bar','baz')
        self.assertEquals(_pass.__name__, route.__name__)

    def testExtractUrlParams(self):
        route = Route(_pass, '/foo', 'bar','baz')
        env = {'PATH_INFO': '/foo/foo/faz'}
        self.assertEquals(route.extract_url_params(env), {'bar': 'foo', 'baz': 'faz'})


