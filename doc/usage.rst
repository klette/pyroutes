Let's do it! (aka Quickstart)
=============================

Application entry point
-----------------------

The application entry point is located directly in the ``pyroutes`` module.
Just do

.. code-block:: python

    from pyroutes import application

in the file you want as a handler for ``mod_wsgi`` or your preferred deployment method.

Adding routes
-------------

Routes are the way for defining which methods should handle requests to which paths.

This is the most basic example::

  from pyroutes import route
  
  @route('/')
  def index(request):
      return Response('Hello world!')

Here we define that our index method should handle all requests to ``/``, and
return the world famous «Hello world!» to the user. 

We can add more routes::

  @route('/sayhello')
  def sayhello(request):
      return Response('Hello %s!' % request.POST.get('name', 'world'))

... Easy as pie!

Route handling gotcha's
^^^^^^^^^^^^^^^^^^^^^^^

After adding the two example routes, we have a handler for ``/`` and ``/sayhello``. If you try
to access ``/foo`` you will get an 404 exception, however if you go to ``/sayhello/foo`` your
request will be passed to the ``sayhello``-method! This is for enabling pretty urls. Pyroutes
will always try to find the most matching handler, except on the root (``/``).


