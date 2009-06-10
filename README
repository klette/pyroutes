pyroutes
=========
A really small wrapper for rapid development of small python
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
That means `@route('/foo/bar')` will always be used over `@route('/foo')`
given that request path is `/foo/bar` or longer that is :-)
Notice that paths have to be given without a trailing slash.

The decorated function should return the helper `Response` class.
The `Response` class takes three arguments: `content`, `headers` and `status_code`.
`content` is the data that should be returned, `headers` a list of tuples representing
the http-headers returned and `status_code` a valid HTTP status code. If `headers` and `status_code`
is omitted it defaults to `text/html` as content type and `200 OK` as status code.

Example:

    @route('/')
    def index(environ, data):
        return(Response('Hello world!', [('Content-Type', 'text/html')], '200 OK'))


Noticed the parameters to the index function? Those are mandatory. 
The `environ`-parameter is the unmodified environment from WSGI and
`data` is a dictionary with the GET and POST parameters.

For more information about usage, see the wiki example.
