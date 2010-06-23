.. _middleware:

Middleware
==========

Middleware is run around each request processing.

In Python we can display this as::

    Outer(Middle(Inner(final_method)))(my param)

Each layer calls the next with the the same parameters as it
was called with, and returns the same. This allows us
to edit requests and responses globally with ease.


Adding middleware
-----------------

Adding middleware is done by modifying the project settings.
See :ref:`pyroutes-settings` for more information about this.


Creating your own
-----------------

Creating your own middleware is quite easy. Let's create
a simple logging middleware as an example.

.. code-block:: python

    import logging

    class LoggingMiddleware(object):
        def __init__(self, passthrough):
	    self.logger = logging.getLogger()
	    self.logger.addHandler(logging.FileHandler('/tmp/mylog.txt'))
	    self.logger.setLevel(logging.DEBUG)
	    self.passthrough = passthrough

	def __call__(self, request):
	    self.logger.debug('Got request %s', request)
	    response = self.passthrough(request)
	    self.logger.debug('Got response %s', response)
	    return response

So, what's going on here?

Every middleware must accept a ``passthrough`` parameter. This is the 
next method in the middleware chain (or the handler itself).
In the ``__call__`` method we accept a mandatory ``request`` parameter,
and return the result of the ``passthrough``-method, called with ``request``
as it's parameter.


