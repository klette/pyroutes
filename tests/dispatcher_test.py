import unittest
import pyroutes
from pyroutes.dispatcher import Dispatcher
from pyroutes.http.request import Request
from pyroutes.http.response import Response
from pyroutes.route import Route
import pyroutes.settings as settings

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

    def test_dispatch(self):
        args_given = [None, None]
        class ArgKeep(object):
            def __init__(self, *args, **kwargs):
                args_given[0] = args
                args_given[1] = kwargs

        def do_test(handler, path, result):
            environment = {'PATH_INFO': path}
            handler = pyroutes.route(path)(handler)
            response = pyroutes.dispatcher.dispatch(environment, ArgKeep)
            self.assertTrue(isinstance(handler, Route))
            self.assertEquals(response, [result])
            self.assertEquals(args_given, [('200 OK', [('Content-Type', 'text/html; charset=utf-8')]), {}])

        do_test(lambda x: Response('result'), '/response1', 'result')
        do_test(lambda x: Response(['result']), '/response2', 'result')

    def test_middleware_chainer(self):
        handler = lambda x: 'result'
        request = Request({})

        self.assertEquals(settings.MIDDLEWARE,
                ('pyroutes.middleware.errors.NotFoundMiddleware',
                'pyroutes.middleware.errors.ErrorHandlerMiddleware'))

        handler = pyroutes.route('/path')(handler)
        result = pyroutes.dispatcher.create_middleware_chain(handler, request)
        self.assertTrue(isinstance(handler, Route))
        self.assertEquals(result, 'result')
