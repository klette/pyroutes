pyroutes
=========
A really small framework for rapid development of small python
web applications

Why?
-----
I got tired of dealing with the same boring WSGI-stuff everytime
I wanted to make a small web-utility in django, but I didn't want
to go to far away from it, so I made this little thing to ease the
work a bit.

How it works
-------------
The core of the system is WSGI, and a decorator called @route.
You simple create add a route decorator in front of the function
you want to handle requests to a certain path. pyroutes always
tries to use the most specified path-handler available for the request.
That means ``@route('/foo/bar')`` will always be used over ``@route('/foo')``
given that request path is ``/foo/bar`` or longer that is :-)
Notice that paths have to be given without a trailing slash.

Example::

    @route('/')
    def index(request):
        return Response('Hello world!')


Templating
----------

pyroutes includes a small xml-based templating system called xml-template.
For more information about xml-template, check out its bzr-repo from 
http://bzr.sesse.net/xml-template
XML-Template is released under the GPLv2 license.


For more information about usage, see the wiki example.
