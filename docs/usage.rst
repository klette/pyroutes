Let's do it! (aka Quickstart)
=============================

All the following examples are also available in the ``examples`` folder of
pyroutes, as ``quickstart.py``.

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

  @route('/')
  def index(request):
      return 'Hello world!'

Here we define that our index method should handle all requests to ``/``, and
return the famous «Hello world!» to the user.

We can add more routes:

.. code-block:: python

  @route('/sayhello')
  def sayhello(request, name='world'):
      return 'Hello %s!' % name

... Easy as pie! Save these at the end of our ``handler.py`` file.

Route handling gotchas
^^^^^^^^^^^^^^^^^^^^^^

After adding the two example routes, we have a handler for ``/`` and
``/sayhello``. If you try to access ``/foo`` you will get an 404 exception.
However, accessing ``/sayhello/master`` does something quite different :)

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
        from pyroutes import utils
        route('/media')(utils.fileserver)
        utils.devserver(application)

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
    $ echo `wget -q -O - http://localhost:8001/sayhello/Pyroutes`
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
    def archive(request, year, month=None, day=None):
        return 'Year: %s  Month: %s  Day: %s' % (year, month, day)

And let's try it::

    $ echo `wget -q -O - http://localhost:8001/archive`
    (This returns Http404 because year is an obligatory parameter)
    $ echo `wget -q -O - http://localhost:8001/archive/2010`
    Year: 2010  Month: None  Day: None
    $ echo `wget -q -O - http://localhost:8001/archive/2010/02`
    Year: 2010  Month: 02  Day: None
    $ echo `wget -q -O - http://localhost:8001/archive/2010/02/03`
    Year: 2010  Month: 02  Day: 03
    $ echo `wget -q -O - http://localhost:8001/archive/2010/02/03/foobar`
    (This returns HTTP 404 because archive only accepts four parameters)

This example should make the URL matching logic clear. Note: If a method
accepts a referenced argument list in the from \*args, it will match any
subpath of its route address.

An example::

    @route('/pathprint')
    def archive(request, *args):
        return 'User requested /%s under /pathprint' % '/'.join(args)

Accessing request data
----------------------

One common operation in developing web applications is doing stuff with user
data.  Pyroutes gives you easy access to the POST, GET and FILES posted to your
request handler.

.. code-block:: python

    @route('/newpost')
    def new_post(request):
        if 'image' in request.FILES:
            # Do stuff with image
            filename, data = request.FILES['image']
            data = data.read()
        category = request.GET.get('category','default')
        title = request.POST.get('title', None)
        if not title:
            return 'No title!'
        return 'OK'

.. note:: If multiple fields have the same name, the value in the respective
          dicts are a list of the given values.

Sending responses to the user
-----------------------------

Every route must return an instance of ``pyroutes.http.response.Response``, or
one of it's subclasses. The former defaults to sending a ``text/html`` response
with status code ``200 OK``. Any data returned that wasn't wrapped in a
Response object will also have these defaults applied (by the Responsify
middleware)

We have the follow built-in responses::

    Response(content=None, headers=None, status_code='200 OK',
            default_content_header=True)

    Redirect(location)

content may be any string or iterable. This means you can do something like this::

    @route('/pdf')
    def pdf(request):
        return Response(open('mypdf.pdf'), [('Content-Type', 'application/pdf')])

Also available for convenience is the HttpException subclasses, also found
under ``pyroutes.http.response``. An example (assuming a method ``decrypt``
that can decrypt files by some algorithm)::

    @route('/decrypt_file')
    def decrypt(request, filename, key):
        full_filename = os.path.join('secrets_folder', filename)
        if not os.path.exists(full_filename):
            raise Http404({'#details': 'No such file "%s"' % filename})
        try:
            return decrypt(full_filename, key)
        except KeyError:
            raise Http403({'#details': 'Key did not match file'})

C is for cookie..
-----------------

Cookies are the de-facto way of storing data on the clients. Pyroutes uses
secure cookies by default. This means that if a user edits his own cookies,
pyroutes will not accept them. This is done by storing a HMAC-signature, based
on the cookie its signing and the ``SECRET_KEY`` in your settings, along with
the actual cookie.

Settings cookies::

    @route('/cookie-set')
    def set_cookies(request, message='Hi!'):
        response = Response('Cookies set!')
        response.cookies.add_cookie('logged_in', 'true')
        # Insecure cookie setting
        response.cookies.add_unsigned_cookie('message', message)
        return response

Retrieving cookies::

    @route('/cookie-get')
    def get_cookies(request):
        logged_in = request.COOKIES.get_cookie('logged_in')
        message = request.COOKIES.get_unsigned_cookie('message')
        if logged_in:
            return message
        raise Http403({'#details': 'Go away!'})

Deleting cookies::

    @route('/cookie-del')
    def get_cookies(request):
        response = Response('Cookies deleted!')
        response.cookies.del_cookie('logged_in')
        response.cookies.del_cookie('message')
        return response


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

    from pyroutes.template import TemplateRenderer

    tmpl = TemplateRenderer('base.xml')

    @route('/')
    def index(request):
        return tmpl.render('index.xml', {})

For more information about XML-Template, see :ref:`xml_template_intro`.
