Reference
=========

:mod:`pyroutes`
---------------

.. module:: pyroutes
   :platform: all
   :synopsis: Core pyroutes public API
.. moduleauthor:: Kristian Klette <klette@samfundet.no>

.. function:: route(path)

   Decorator for declaring a method as a handler for a specific path, and paths
   above it if no better match exists. The decorated method should take an
   instance of :mod:`pyroutes.http.request.Request` as its first argument, and
   optionally more arguments auto-populated from the path.

   All handler methods must return an instance of
   :mod:`pyroutes.http.response.Response`.


.. function:: reverse_url(handler)

   Return the path a handler is responible for.

   Example::

       pyroutes.route('/foo/bar')
       def foo_method(request):
           return Response("foo")
       pyroutes.reverse_url('foo_method')
       '/foo/bar'

:mod:`pyroutes.http.response`
-----------------------------

.. module:: pyroutes.http.response
   :synopsis: Pyroutes response types
.. moduleauthor:: Kristian Klette <klette@samfundet.no>

.. class:: Response([content=None, headers=none, status_code='200 OK',
	default_content_header=True])

   :param content: Initial content. Must be an iterable.
   :param headers: List of tuples with the headers.
   :param status_code: Initial status code of the response.
   :param default_content_header: Set the default content header from ``pyroutes.settings`` to the response.

   .. attribute:: cookies
      Instance of :mod:`pyroutes.http.cookies.ResponseCookieHandler`



