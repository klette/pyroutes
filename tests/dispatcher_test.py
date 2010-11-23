import unittest
import pyroutes
from pyroutes.dispatcher import Dispatcher

class TestDispatcher(unittest.TestCase):

    def createAnonRoute(self, path):
        @pyroutes.route(path)
        def foo(bar, baz):
            pass
        return foo

    def createClassAnonRoute(self, path):
        class Foo(object):
            @pyroutes.route(path)
            def foo(req, baz):
                pass

    def testFindRequestHandler(self):
        dispatcher = Dispatcher()
        self.createAnonRoute('/')
        self.createAnonRoute('/bar/baz/foo')
        self.createAnonRoute('/baz')
        self.createClassAnonRoute('/class')
        self.assertTrue(dispatcher.find_request_handler('/foo') == None)
        self.assertTrue(dispatcher.find_request_handler('/') != None)
        self.assertTrue(dispatcher.find_request_handler('/bar/baz/foo') != None)
        self.assertTrue(dispatcher.find_request_handler('/baz/param') != None)
        self.assertTrue(dispatcher.find_request_handler('/class') != None)
        self.assertTrue(dispatcher.find_request_handler('') != None)
