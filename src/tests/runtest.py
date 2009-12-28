import sys
from os import path

from CoverageTestRunner import CoverageTestRunner

sys.path.insert(0, path.join(path.dirname(__file__), '..'))

r = CoverageTestRunner()

r.add_pair("pyroutes/__init__.py", "tests/routestest.py")
r.add_pair("pyroutes/http.py", "tests/httptest.py")
r.add_pair("pyroutes/utils.py", "tests/utilstest.py")
r.run()
