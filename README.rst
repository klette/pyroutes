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

Example::

    @route('/')
    def index(request, name='world'):
        return Response('Hello %s!' % name)

    GET /
    Hello world!

    GET /foo
    Hello foo!


See http://readthedocs.org/docs/pyroutes/ for more information.


Templating
----------

pyroutes includes a small xml-based templating system called xml-template.
For more information about xml-template, check out its bzr-repo from 
http://bzr.sesse.net/xml-template
XML-Template is released under the GPLv2 license.


For more information about usage, see the wiki example.
