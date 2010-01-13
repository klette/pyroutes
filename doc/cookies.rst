Cookies
=======

pyroutes provides some basic utilities for dealing with cookies. All cookies
are signed using HMAC authentication, but it possible to not use the signed
cookies. This is not recommended though as unsigned cookies gives no guarantee
that the cookie hasn't been tampered with by the user or some entity between
the user and your web application.

The HMAC is generated with the `SECRET_KEY` from `pyroutes.settings`, so be
sure to set it to something long and random in your per-site settings
(`pyroutes_settings`).

Adding cookies
--------------

Adding cookies is done on the `Response.cookies`-object.

Example:

::

    response = Response()
    response.cookies.add_cookie('username', 'my_awesome_username')
    response.cookies.add_unsigned_cookie('unsafe_key', 'unsafe_value')

This code will add three cookies to the HTTP-headers returned to the client.
One for each key/value pair, and one for the secure hash of the signed cookie.

Reading cookies
---------------

Reading back the cookies is done on the `Request.COOKIES`-object.

Example:

::

   @route('/')
   def index(request):
       username = request.COOKIES.get_cookie('username')
       not_trusted = request.COOKIES.get_unsigned_cookie('foobar')
       if not username:
           return Redirect('/login')
       return Response('Welcome %s' % username)



Cookie API
----------

:mod:`pyroutes.http.response.Response.cookies`

.. method:: add_cookie(key, value, expires=None)

Adds a signed cookie to the response object. The key may _not_ include a "="-sign in
it. The value is put directly in the cookie, so if you're adding some data that
is non-trivial, you should base64-encode it or similar. The expires variabel
takes any `datetime`-object.

.. method:: add_unsigned_cookie(key, value, expires=None)

Adds a unsigned cookie. The variables is treated the same way as in `add_cookie(..)`


:mod:`pyroutes.http.request.Request.COOKIES`

.. method:: get_cookie(key)

Returns the value for the key. None if it does not exists.
Throws an `CookieHashMissing` exception if the hash cookies has been removed,
and an `CookieHashInvalid` if the data has been tampered with.

.. method:: get_unsigned_cookie(key)

Returns the value for the key. None if it does not exists.

.. data:: COOKIES._raw_cookies

A dictionary containing all the cookies for this domain. This is the raw
cookies and no validation of the hashes are done. So use this with care.

