#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages
import os

setup(
    name = "pyroutes",
    version = "0.1.2",
    url = 'http://github.com/klette/pyroutes',
    license = 'GPLv2',
    description = "A small WSGI wrapper for creating small python web apps",
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    author = 'Kristian Klette',
    author_email = 'klette@samfundet.no',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],

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

