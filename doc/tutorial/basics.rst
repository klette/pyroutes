Tutorial - Part 1 - The basics
===============================

This tutorial will take you through the basics of creating a pyroutes-based web
application.

Let's start by creating the enviroment for developing our application.

::

    mkdir tutorial
    cd tutorial

Application entrypoint and development server
---------------------------------------------

The first thing we need is something to launch our application. We'll create a
wsgi-file which can be used by `mod-wsgi`, but also include a basic webserver
for testing our code without launching apache or another large webserver.

Create a file called `server.wsgi`::

    from wsgiref.simple_server import make_server
    from pyroutes import application

    if __name__ == '__main__':
        make_server('', 8080, application).serve_forever()

You may now run this file as using python and it will launch our development
server on your host on port 8080.  If your developing locally you can launch
your browser and go to http://localhost:8080 and you'll get a 404-page
complaining about no handler found. If you're developing on a server, replace
localhost with the hostname or ip of the server.

Note that the server will not reload itself as you develop more code, so you'll
either have to restart the server each time you want to check your code, or
deploy your application behind apache. See :ref:`deployment/apache` for
information about deployment.

Hello world
-----------

We can now start developing something to show to the user. Let's start by
creating a simple Hello World-app.

Create a file called hello.py::

    from pyroutes import route
    from pyroutes.http.respone import Response

    @route('/')
    def say_hello(request):
        return Response('Hello World')

We start by including the route decorator. This is the way that pyroutes maps
paths to handler functions.  We also include the Response-class from
:mod:`pyroutes.http.response`, which is a helper-class for returning a response
to the user.

We define a method called `say_hello`, all request handlers get two parameters
from pyroutes. The first argument is the WSGI-enviroment-instace for that
request, and the second is a dictionary with everything posted to the request
as either a `GET` or `POST` variabel. The method is decorated with the `route`
decorator with the wanted path as the only argument, in our case `/`. The
method only returns a simple `Response`-instance with 'Hello World' as content.
The `Response`-class defaults to send `text/html` as `Content-Type` and `200
OK` as HTTP status code.

Here is a bit of a gotcha, to have this enabled by our application, it must be
included at compiletime (not really, but let's assume that for the purpose of
this intro tutorial). So we'll have to import our hello-script in
`server.wsgi`. We do this simply by adding `import hello` below our other
imports.

If you restart your development server and point your browser to
http://localhost:8080/ you should see "Hello World" on your screen.

Congratulation, you've just created your first pyroutes based web application!

Templating
----------

Web development without templates is really not a good idea, so pyroutes
includes a xml-based templating system called xml-template.  It's quite
different from most templating systems as is solely based upon XML, and does
not include any logic functionality in the template-code, but you'll get used
to that after a while, I promise.

pyroutes is aimed at small web applications, and most of the application made
only make use of a base-template for the XHTML-boilerplate code, css,
javascript and all that jazz, and a template inside that for content. So
pyroutes includes a helper for doing exactly that using xml-template.

Let's dive into it! Create a file called `base.xml`

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

     <html xmlns="http://www.w3.org/1999/xhtml" xmlns:t="http://template.sesse.net/" xml:lang="en">
       <head>
         <title>pyroutes demo</title>
       </head>

        <body>
          <h1>pyroutes demo</h1>
          <t:contents />
        </body>
      </html>

As you can see this is a pretty basic XHTML file. There is one special element
here though; the `<t:contents />`-tag. This must be available in all base
templates pyroutes uses, as it will be replaced with the content.

So let's create a content template. Create a file called `content.xml`

.. code-block:: xml

    <t:dummy xmlns:t="http://template.sesse.net/">
      <p t:id="message" />
    </t:dummy>

As each template file must be valid XML we wrap the contents in a dummy-node.
You might notice that we've added a parameter to the `<p>`-tag, `t:id`. This is
the way we identify parts of the XHTML from the python code.

Now, let us create a request handler to use the templates.

.. code-block:: python

    from pyroutes import route
    from pyroutes.http.response import Response
    from pyroutes.template import TemplateRenderer

    tmpl_renderer = TemplateRenderer('base.xml')

    @route('/)
    def templated_handler(request):
        template_data = {'#message': 'Hello World'}

        return Response(tmpl_renderer.render('content.xml', template_data))

As you can see we imported `TemplateRenderer` from :mod:`pyroutes.template`,
and initialized it with our base template as the only parameter. This will make
the `TemplateRenderer`-instance render what it's given and replace the
`<t:contents />`-tag in the base template with it.

To `TemplateRenderer`'s `render`-method we in addition to the template we want
to render inside our base template, pass a dictionary with the data the
content-template should use. The syntax is pretty simple

.. code-block:: python

    data = {
        '#message': 'foobar', # Replaces the content of the tag with t:id='message' with 'foobar'
        '#message/class': 'message', # Replaces or adds the class-attribute to the tag with t:id='message' to 'message'
        'msg': 'hello' # Replaces any <t:msg />-tag with 'hello' in the template.
	 }

One thing most people struggle with when starting to use xml-template is
creating lists of things. Here is how to do that.

.. code-block:: xml

    <ul t:id="entries">
      <li t:id="entry" />
    </ul>

.. code-block:: python

    data = {
    	'#entries': [
    	              {'#entry': 'entry 1'},
    	              {'#entry': 'entry 2'},
    	              {'#entry': 'entry 3'},
    		    ]
          }

For more xml-template examples see http://bzr.sesse.net/xml-template/.

Getting input from the user
---------------------------

One common operation in web applications is getting input from the user, pyroutes handles
this by providing every route with a :mod:`pyroutes.http.request.Request`-object.
This object provides you, among other things, a `POST` and a `GET` dictionary containing
the values from the user.

Here is a simple example:

.. code-block:: python

    @route('/sayhello')
    def sayhello(request):
        name = request.GET.get('name', None)
	if name:
	    return Response('Hello %s!' % name)
        else:
	    return Response('I don\'t know your name yet')


That should get you started in your development of a pyroutes powered application. Good luck!
