import unittest
import minimock
import cgi

import pyroutes


class TestRoute(unittest.TestCase):
    def setUp(self):
        pyroutes.__request__handlers__ = {}


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

    #TODO: Add environ-fixture and test for real! :-)
    def testCreateDataDict_no_data(self):
        cgi.FieldStorage = minimock.Mock('cgi.FieldStorage', returns={}, tracker=None)
        self.assertTrue(pyroutes.create_data_dict({'wsgi.input': None}) == {})
    
    #TODO: Add environ-fixture and test for real! :-)
    def testCreateDataDict_with_data(self):
        
        datamock = minimock.Mock('datamock', tracker=None, returns={'foo': None})
        datamock.keys = minimock.Mock('datamock.keys', tracker=None, returns=['foo'])
        datamock.getvalue = minimock.Mock('datamock.getvalue', tracker=None, returns='bar')
        
        cgi.FieldStorage = minimock.Mock('cgi.FieldStorage', returns=datamock, tracker=None)
        self.assertEquals(pyroutes.create_data_dict({'wsgi.input': None}), {'foo': 'bar'})

    def testApplication404(self):
        environ = {'PATH_INFO': '/'}
        tracker = minimock.TraceTracker()
        start_response = minimock.Mock('start_response', tracker=tracker)

        self.assertEquals(["No handler found for path //"], pyroutes.application(environ, start_response))
        self.assertTrue(tracker.check("Called start_response('404 Not Found', [('Content-type', 'text/plain')])"))

    def testApplication200(self):
        environ = {'PATH_INFO': '/'}
        tracker = minimock.TraceTracker()
        start_response = minimock.Mock('start_response', tracker=tracker)

        pyroutes.create_data_dict = minimock.Mock('create_data_dict', returns={}, tracker=None)
        res = minimock.Mock('handler', tracker=None)
        res.content = "foobar"
        res.status_code = '200 OK'
        res.headers = [('Content-type', 'text/plain')]

        handler = minimock.Mock('handler', tracker=None, returns=res)

        # Manually inject handler
        pyroutes.__request__handlers__['/'] = handler
        tracker.clear()
        self.assertEquals(["foobar"], pyroutes.application(environ, start_response))
        self.assertTrue(tracker.check("Called start_response('200 OK', [('Content-type', 'text/plain')])"))
        res.content = (1,2,3)
        self.assertEquals((1,2,3), pyroutes.application(environ, start_response))

    def testApplication500(self):
        environ = {'PATH_INFO': '/'}
        tracker = minimock.TraceTracker()
        start_response = minimock.Mock('start_response', tracker=tracker)

        pyroutes.create_data_dict = minimock.Mock('create_data_dict', returns={}, tracker=None)
        handler = minimock.Mock('handler', tracker=None)
        handler.mock_raises = ValueError("foo")
        pyroutes.__request__handlers__['/'] = handler
        tracker.clear()
        response = pyroutes.application(environ, start_response)
        self.assertNotEqual(response[0].find('Server error at /.'), -1)
        self.assertTrue(tracker.check("Called start_response('500 Server Error', [('Content-Type', 'text/html; charset=utf-8')])"))
        tracker.clear()
