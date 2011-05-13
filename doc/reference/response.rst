Request and response objects
============================

.. module:: pyroutes.http
   :synopsis: Pyroutes request and response classes

Overview
--------

All handlers and middleware receive an instance
of the Request class and must return an instance
of the Response class.

This document explains the APIs for :class:`Response`
and :class:`Request`.



.. module:: pyroutes.http.request

Request objects
---------------

.. class:: Request

Attributes
^^^^^^^^^^

.. attribute:: Request.GET

   A dictionary of the given GET variables.

.. attribute:: Request.POST

   A dictionary of the given ``POST`` variables. If a multiple
   key-value pairs has the same key name, the dictionary value
   for the key will be a list of the values.

.. attribute:: Request.FILES

   A dictionary of the given files. As with the ``POST`` variables,
   multiple keys with the same name will result in a list.
   The values are tuples consisting of the filename and a file-like object.

.. attribute:: Request.COOKIES

   An instance if ``RequestCookieHandler`` which provides the following
   API.

   .. method:: get_cookie(key)

      Return the value of a signed cookie, or None if it doesn't exist.
      Raises ``CookieHashInvalid`` or ``CookieHashMissing`` if the
      user has altered the cookies in any way.


   .. method:: get_unsigned_cookie(key)

      Return the value of a cookie without validating it's authenticity.
      Returns None if the cookie doesn't exist.

.. attribute:: Request.ENV

   The environment as passed from ``WSGI``.


.. module:: pyroutes.http.response

Response objects
----------------

.. class:: Response([content=None, headers=None, status_code='200 OK',
        default_content_header=True])

The base response class. Constructor initializes the attributes with its given
values. If ``default_content_header`` is true, and ``Content-Type`` is not
passed in headers, the content type defined in
``pyroutes.settings.DEFAULT_CONTENT_TYPE`` will be added to the headers
automatically.

The status code can be passed as ``either`` a full status code ``or`` an
integer corresponding to a standard code.

Attributes
^^^^^^^^^^

.. attribute:: Response.content

   A string or an iterable object that is passed to the browser.

.. attribute:: Response.status_code

   The HTTP status code sent to the client. Can be either a full string
   representation of the status code, or just the number id.

.. attribute:: Response.headers

   A list of tuples with key-value pairs of headers and their value.

.. attribute:: Response.cookies

   An instance of ``ResponseCookieHandler`` which provides the following API.

   .. method:: add_cookie(key, value[, expires=None])

      Adds a signed cookie to the response. The ``expires`` parameter must be
      an instance of ``datetime.datetime`` and set the cookie expiration to
      its value. Defaults to infinite lifetime.

   .. method:: add_unsigned_cookie(key, value[, expires=None])

      Same functionality as ``add_cookie`` only the cookie will not be signed,
      and is not tamper proof.

   .. method:: del_cookie(key)

      Deletes a cookie from the browser.


Redirect objects
----------------

.. class:: Redirect(location[, absolute_path=False])

A redirect shortcut class for redirection responses. This class can make two types of redirects:

     1. Absolute path redirects: When you want do redirect to outside your
        application.
     2. Root App relative redirect: If you want your redirection relative to
        the root application path.
     3. Site relative redirect: If you want your redirection relative to the
        base of the domain.
     4. Current URL relative redirect: If you want your redirection relative to
        the current URL value.

Example of these uses, assuming your app is installed on
``http://example.com/apps/myapp``:

     1. ``Redirect('http://pyroutes.com/')`` for a redirect to pyroutes.com.
     2. ``Redirect('/some/path')`` for a redirect to
        ``http://example.com/apps/myapp/some/path``.  Ignores current URL.
     3. ``Redirect('/other/path', absolute_path=True)`` to redirect to
        ``http://example.com/other/path``. Ignores current URL.
     4. ``Redirect('relative/path')`` to redirect to a path relative to the
        current URL of the user's browser. E.g. if the user is visiting
        ``http://example.com/apps/myapp/foo/`` this redirect would go to
        ``http://example.com/apps/myapp/foo/relative/path``


HttpException objects
---------------------

.. class:: HttpException(location[, \*\*template_data])

Base class for all exceptions that produce special error pages. If instances of
objects that inherited from HttpException are raised, the
ErrorHandlerMiddleware will render a page and return it with the correct HTTP
code. The base template can be overriden using settings.CUSTOM_BASE_TEMPLATE
and additional template data kan be passed to the exception. Raising a
HttpException without passing a location as first parameter is allowed,
location is then populated from the PATH_INFO variable.

.. class:: Http403

Template for this HttpException can be overridden using settings.TEMPLATE_403

.. class:: Http404

Template for this HttpException can be overridden using settings.TEMPLATE_404

.. class:: Http500

Template for this HttpException can be overridden using settings.TEMPLATE_500
