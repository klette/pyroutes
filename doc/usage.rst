Let's do it! (aka Quickstart)
=============================

Application entry point
-----------------------

The application entry point is located directly in the ``pyroutes`` module.
Just do

.. code-block:: python

    from pyroutes import application

in the file you want as a handler for ``mod_wsgi`` or your preferred deployment method.
Let's call it ``handler.py`` for now.

Adding routes
-------------

Routes are the way for defining which methods should handle requests to which paths.

This is the most basic example::

  from pyroutes import route
  from pyroutes.http.response import Response
  
  @route('/')
  def index(request):
      return Response('Hello world!')

Here we define that our index method should handle all requests to ``/``, and
return the world famous «Hello world!» to the user. 

We can add more routes::

  @route('/sayhello')
  def sayhello(request):
      return Response('Hello %s!' % request.GET.get('name', 'world'))

... Easy as pie! Save these at the end of our ``handler.py`` file.

Route handling gotcha's
^^^^^^^^^^^^^^^^^^^^^^^

After adding the two example routes, we have a handler for ``/`` and
``/sayhello``. If you try to access ``/foo`` you will get an 404 exception,
however if you go to ``/sayhello/foo`` your request will be passed to the
``sayhello``-method! This is for enabling pretty urls. Pyroutes will always try
to find the most matching handler, except on the root (``/``).

Starting the development server
-------------------------------

Pyroutes includes a development server to ease local development quite a bit.
It's located in the ``pyroutes.utils`` module.

Using it is as easy as adding this to ``handler.py`` from the previous
examples.::

    if __name__ == '__main__':
        from pyroutes.utils import devserver
        devserver(application)

Serving static media
^^^^^^^^^^^^^^^^^^^^

Static media is normally served directly from the web server, but we need
static files when developing locally as well. You can serve static files through
the devserver using the ``fileserver`` route in ``pyroutes.utils``. Change the
previous code to something like this::

    if __name__ == '__main__':
        from import utils
        route('/media')(utils.fileserver)
        devserver(application)

This will now serve anything you have in the folder called ``media`` in your
working directory in the ``/media`` path. This behaviour can be modified in
``pyroutes_settings``.

Firing it up
------------

Let's try what we have so far. Open up a terminal, go to the directory where
you saved the ``handler.py`` file, and execute it::

    $ python handler.py
    Starting server on 0.0.0.0 port 8001...

Your application should now be running on port 8001. Let's try it.::

    $ echo `wget -q -O - http://localhost:8001/`
    Hello world!
    $ echo `wget -q -O - http://localhost:8001/sayhello?name=Pyroutes`
    Hello Pyroutes!


Debugging
---------

If something in the code was not correct, and an exception was thrown, you'll
get a error page with not much information. You can see more about what went
wrong if you enable pyroutes' debugging.

This is done by creating a file called ``pyroutes_settings.py`` in your
``PYTHONPATH``. Create this file and add::

    DEBUG=True

Now refresh the page with the error, and you'll get a lot more information to work with.

Using URLs as data
------------------

As of Pyroutes >= 0.3.0 using URLs as data for your handler really simple.
Let's create an ``archive`` route as an example::

    @route('/archive')
    def archive(request, year, month, day):
        return Response('Year: %s  Month: %s  Day: %s' % (year, month, day))

And let's try it::

    $ echo `wget -q -O - http://localhost:8001/archive`
    Year: Month: Day:
    $ echo `wget -q -O - http://localhost:8001/archive/2010`
    Year: 2010 Month: Day:
    $ echo `wget -q -O - http://localhost:8001/archive/2010/02`
    Year: 2010 Month: 02 Day:
    $ echo `wget -q -O - http://localhost:8001/archive/2010/02/03`
    Year: 2010 Month: 02 Day: 03
    $ echo `wget -q -O - http://localhost:8001/archive/2010/02/03/foobar`
    Year: 2010 Month: 02 Day: 03

It's important to know that variables not available from the URL is passed to
your method as an empty string or your defined default in the method
declaration.

Accessing request data
----------------------

One common operation in developing web applications is doing stuff with user
data.  Pyroutes gives you easy access to the POST, GET and FILES posted to your
request handler.

::

    @route('/newpost')
    def new_post(request):
        if 'image' in request.FILES:
	    # Do stuff with image
	    filename = request.FILES['image'][0]
	    data = request.FILES['image'][1].read()
	    pass
	category = request.GET.get('category','default')
	title = request.POST.get('title', 'None')
	if not title:
	    return Response('no title!')
	return Response('OK')

.. note:: If multiple fields have the same name, the value in the respective
          dicts are a list of the given values.

Sending responses to the user
-----------------------------

Every route must return an instance of ``pyroutes.http.response.Response``, or
one of it's subclasses. The former defaults to sending a
``text/html``-response with status code ``200 OK``.

We have the follow built-in responses::

    Response(content=None, headers=None, status_code='200 OK',
    	default_content_header=True)

    Redirect(location)

content may be any string or iterable. This means you can do something like this::

    @route('/pdf')
    def pdf(request):
        buffer = cStringIO.StringIO()
        with open("mypdf.pdf", "rb") as pdf_file:
            buffer.write(pdf_file.read())
        return Response(buffer, [('Content-Type', 'application/pdf')],
            default_content_header=False)



C is for cookie..
-----------------

Cookies are the de-facto way of storing data on the clients. Pyroutes uses
secure cookies by default. This means that if a user edits his own cookies,
pyroutes will not accept them. This is done by storing a HMAC-signature, based
on the cookie its signing and the ``SECRET_KEY`` in your settings, along with
the actual cookie.

Settings cookies::

    @route('/cookie-set')
    def set_cookies(request):
        response = Response()
        response.cookies.add_cookie('logged_in', 'true')
        # Insecure cookie setting
        response.cookies.add_unsigned_cookie('blapp', 'foo')
        return response

Retrieving cookies::

    @route('/cookie-get')
    def get_cookies(request):
        logged_in = request.COOKIES.get_cookie('logged_in')
        blapp = request.COOKIES.get_unsigned_cookie('blapp')
        if logged_in:
            return Response('Hi!')
        return Response('Go away!')



Let's go templates!
-------------------

Pyroutes bundles XML-Template, a template system created by Steinar H.
Gunderson, which might seem a bit «chunky», but it really fast, and guarantees
it's output to be valid XML (or in our case XHTML). The big difference between
XML-template and most other template systems out there, is that XML-template is
purely a representation layer. You don't have any logic in your templates.

Now, pyroutes has a small wrapper around XML-Template for handling the most
common template task; having a base-template, and a separate template for your
current task.::

    from pyroutes.templates import TemplateRenderer

    tmpl = TemplateRenderer('base.xml')

    @route('/')
    def index(request):
    	return Response(tmpl.render('index.xml', {}))

For more information about XML-Template, see :ref:`xml_template_intro`.
