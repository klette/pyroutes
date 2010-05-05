.. _ref-request-and-response

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

The base response class. Constructor initializes the attributes with its
given values. If ``default_content_header`` is true, the content type
defined in ``pyroutes.settings.DEFAULT_CONTENT_TYPE`` will be added
to the headers automatically.

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
