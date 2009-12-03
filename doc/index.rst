.. pyroutes documentation master file, created by sphinx-quickstart on Tue Dec  1 14:58:22 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyroutes
========

pyroutes is a really small framework (more of a wrapper really) around wsgi for
developing small python web apps.

If you're developing a larger project, I suggest you point your browser to http://djangoproject.com instead :-)


Tutorials
=========

Contents:

.. toctree::
   :maxdepth: 2

   tutorial/basics
   tutorial/wiki


Installation
============

pyroutes is available trough pypi and is easily installed by using either pip or easy_install.

Installation with pip::

  # pip install pyroutes

Installation with easy_install::

  # easy_install pyroutes


Deployment
==========

.. toctree::
   :maxdepth: 1

   deployment/apache

Contributing
============

The source code is version controlled using git and resides on http://github.com/klette/pyroutes. Feel free to clone it
and fix stuff :-) Just remember to check if the test-suite still passes. I will not pull in features if they don't include
documentation, unittest or simply breaks the existing tests. Bugfixes to the tests are always welcome too though.


Module documentation
====================

.. toctree::
   :maxdepth: 2

   modules/pyroutes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

