#!/bin/env python

import os
import sys
import uuid

try:
    from hashlib import sha1
except:
    import sha1

if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    sys.stderr.write("usage: pyroutes-admin.py projectname\n")
    sys.stderr.flush()
    sys.exit(1)

project = sys.argv[1]
project_path = os.path.join(os.getcwd(), project)

if os.path.exists(project_path):
    sys.stderr.write("File or folder with the same name as the project exists.. exiting.\n")
    sys.stderr.flush()
    sys.exit(1)

# Create project directories
os.mkdir(project_path)
os.mkdir(os.path.join(project_path, project))
os.mkdir(os.path.join(project_path, 'templates'))
os.mkdir(os.path.join(project_path, 'tests'))

# Initialize project module
f = open(os.path.join(project_path, project, '__init__.py'), 'w')
f.write("\n")
f.close()

# Create project settings
f = open(os.path.join(project_path, 'pyroutes_settings.py'), 'w')
f.write('import os\n\n')
f.write('SECRET_KEY = \'%s\'\n' % sha1(str(uuid.uuid4())).hexdigest())
f.write('TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), \'templates\')')
f.flush()
f.close()

# Create basic handler.py
f = open(os.path.join(project_path, 'handler.py'), 'w')
f.write('#!/bin/env python\n\nfrom pyroutes import application\n\n')
f.write('from %s import *\n\n' % project)
f.write('if __name__ == \'__main__\':\n    from pyroutes.utils import devserver\n')
f.write('    devserver(application)\n')
f.flush()
f.close()

sys.stdout.write("Done. Go hacking!\n")
sys.stdout.flush()

sys.exit(0)
