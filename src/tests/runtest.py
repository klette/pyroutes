import sys
from os import path, chdir

from CoverageTestRunner import CoverageTestRunner

r = CoverageTestRunner()

base_dir = path.abspath(path.join(path.dirname(__file__), '..'))
chdir(base_dir)
sys.path.insert(0, base_dir)

mapping = (
    ('__init__.py', 'routestest.py'),
    ('http.py', 'httptest.py'),
    ('utils.py', 'utilstest.py')
)

for pair in mapping:
    r.add_pair(path.join('pyroutes', pair[0]), path.join('tests', pair[1]))

r.run()
