.. pyroutes documentation master file, created by sphinx-quickstart on Tue Dec  1 14:58:22 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyroutes
========

pyroutes is a really small framework (more of a wrapper really) around wsgi for
developing small python web apps.

If you're developing a larger project, I suggest you point your browser to http://djangoproject.com instead :-)


User manual
===========

Contents:

.. toctree::
   :maxdepth: 2

   installation
   usage
   deployment

Appendices
==========

.. toctree::
    :maxdepth: 2

    appendix/xmltemplate

Release change logs
==================

.. toctree::
   :maxdepth: 2

   changelog

Contributing
============

The source code is version controlled using git and resides on http://github.com/klette/pyroutes. Feel free to clone it
and fix stuff :-) Just remember to check if the test-suite still passes. I will not pull in features if they don't include
documentation, unittest or simply breaks the existing tests. Bugfixes to the tests are always welcome too though.

For the tests to run, you will need some extra packages. Names are by
debian/ubuntu package name.

 * python-minimock, http://blog.ianbicking.org/minimock.html
 * python-coverage, http://nedbatchelder.com/code/coverage/
 * python-nose

