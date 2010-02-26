import unittest
import sys

from routestest import TestRoute 
from utilstest import *

import xmlrunner

suite = unittest.TestSuite([
unittest.TestLoader().loadTestsFromTestCase(TestRoute),
unittest.TestLoader().loadTestsFromTestCase(TestDevServer),
unittest.TestLoader().loadTestsFromTestCase(TestFileServer),
])

if __name__ == '__main__':
    runner = xmlrunner.XmlTestRunner(sys.stdout)
    runner.run(suite)
