from CoverageTestRunner import CoverageTestRunner

r = CoverageTestRunner()

r.add_pair("pyroutes/__init__.py", "tests/routestest.py")
r.run()
