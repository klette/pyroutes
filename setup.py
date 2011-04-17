#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup
import os

setup(
    name = "pyroutes",
    version = "0.4.0",
    url = 'http://github.com/pyroutes/pyroutes',
    license = 'GPLv2',
    description = "A small WSGI wrapper for creating small python web apps",
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author = 'Kristian Klette',
    author_email = 'klette@samfundet.no',
    packages = ['pyroutes','pyroutes.http', 'pyroutes.template', 'pyroutes.contrib', 'pyroutes.middleware'],
    requires = ['wsgiref'],
    package_data = {'pyroutes': ['default_templates/*.xml', 'default_templates/fileserver/*.xml']},
    scripts = ['bin/pyroutes-admin.py'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        ]

)

