import unittest
import sys

from routestest import *
from utilstest import *
from responsetest import *
from cookietest import *

import xmlrunner

suite = unittest.TestSuite([
unittest.TestLoader().loadTestsFromTestCase(TestRoute),
unittest.TestLoader().loadTestsFromTestCase(TestDevServer),
unittest.TestLoader().loadTestsFromTestCase(TestFileServer),
unittest.TestLoader().loadTestsFromTestCase(TestResponse),
unittest.TestLoader().loadTestsFromTestCase(TestExceptions),
unittest.TestLoader().loadTestsFromTestCase(TestRequestCookieHandler),
unittest.TestLoader().loadTestsFromTestCase(TestResponseCookieHandler),
])

if __name__ == '__main__':
    runner = xmlrunner.XmlTestRunner(sys.stdout)
    runner.run(suite)
