import unittest
import pyroutes
from pyroutes.dispatcher import Dispatcher
from pyroutes.http.request import Request
from pyroutes.http.response import Response
from pyroutes.route import Route
import pyroutes.settings as settings

class TestDispatcher(unittest.TestCase):

    SCRIPT_NAME  = '/path/to/the/app/root'
    SITE_ROOT_ATTR_NAME = 'SITE_ROOT'

    def start_response(self, status_code, headers):
      pass

    def setUp(self):
      self.ENV = {
           'SCRIPT_NAME': self.SCRIPT_NAME,
           'PATH_INFO': '/path'
           }
      self.dispatcher = Dispatcher()
      if hasattr(settings, self.SITE_ROOT_ATTR_NAME):
        delattr(settings, self.SITE_ROOT_ATTR_NAME)

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

    def testUpdateApplicationRootValue(self):
      self.dispatcher.dispatch(self.ENV, self.start_response)
      self._check_settings_attribute('SITE_ROOT', self.SCRIPT_NAME)

    '''
       Remove the trailing slash so we can use "/".join() when
       building the full application path
    '''
    def testUpdateApplicationRootValueNoTrailingSlash(self):
      self.ENV['SCRIPT_NAME'] = '/some/path/with/trailing/slash/'
      self.dispatcher.dispatch(self.ENV, self.start_response)
      self._check_settings_attribute(self.SITE_ROOT_ATTR_NAME, '/some/path/with/trailing/slash')
      


    '''
      Ensure that an empty value is used when SCRIPT_NAME is absent
    '''
    def testUpdateApplicationRootEmptyValue(self):
      self.ENV['SCRIPT_NAME'] = ''
      self.dispatcher.dispatch(self.ENV, self.start_response)
      self._check_settings_attribute(self.SITE_ROOT_ATTR_NAME, '')

    def testDoNotUpdateApplicatinRootIfAlreadyExist(self):
      settings.SITE_ROOT = '/some/path'
      self.dispatcher.dispatch(self.ENV, self.start_response)
      self.assertEquals(settings.SITE_ROOT, '/some/path')

    '''
      Don't panic if we don't have a SCRIPT_NAME value.
    '''
    def testUpdateApplicationRootAbsentValue(self):
      del self.ENV['SCRIPT_NAME']
      self.dispatcher.dispatch(self.ENV, self.start_response)
      self._check_settings_attribute(self.SITE_ROOT_ATTR_NAME, '')


    def _check_settings_attribute(self, attr_name, attr_value):
      self.assertTrue('pyroutes.settings does no have attribute %s' % attr_name, hasattr(settings, attr_name))
      self.assertEquals(attr_value, getattr(settings, attr_name))

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
