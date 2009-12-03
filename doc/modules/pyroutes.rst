:mod:`pyroutes`
================

.. module:: pyroutes
   :platform: All
   :synopsis: Core pyroutes module
.. moduleauthor:: Kristian Klette <klette@samfundet.no>

This module holds the core functionality of pyroutes.

API
---

.. method:: route(path)

This is a decorator that assigns the decorated method to act as a handler for the given `path`.
Raises an `ValueError`-exception if an existing handler for that `path` is already defined.

Example usage::

    from pyroutes import route
    from pyroutes.http import Response
    
    @route('/hello')
    def hello(env, params):
        return Response('Hello!')


.. method:: application(..)

This is the entrypoint for wsgi. Import this in your .wsgi-file, and point apache or similar to it.

Example .wsgi file::

    from pyroutes import application

    # We don't need anything else in here.. sweet.

Internal storage
-----------------
.. data:: __request__handlers__

The global path to handler dictionary. Provides storage for the dispatcher and route-decorator.


