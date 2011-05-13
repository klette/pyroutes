.. _pyroutes-settings:

Settings
========

Pyroutes enables you to have per project settings by overriding
``pyroutes.settings`` in a file called ``pyroutes_settings.py`` in your
``PYTHON_PATH``.

The following settings are defined and can be overridden:

.. attribute:: DEBUG

   Enables debugging output on the ``500 Server Error``. Should
   not be true in production, as it might leak sensitive data.

   **Default**: False

.. attribute:: DEFAULT_CONTENT_TYPE

   The default content type set by ``Response``.

   **Default**: `'text/html; charset=utf8'`

.. attribute:: SECRET_KEY

   Key for cryptographic functions in pyroutes.  You *must* override this in
   your per project settings for the crypto to add any value.


.. attribute:: TEMPLATE_DIR

   The location of the filesystem ``TemplateRenderer`` looks for
   the templates. If set to None it will try to load from the current
   working directory.

   **Default**: None


.. attribute:: MIDDLEWARE

   A list of the enabled middlewares to be run, from outer to inner.
   You most likely want to keep the default middleware classes if enabling more
   middleware. Also, note that for the ErrorHandlerMiddleware to handle errors
   it *must* be the last element of the list.

   You can read more about middleware here :ref:`middleware`.

   **Default**: ``('pyroutes.middleware.errors.NotFoundMiddleware',
   'pyroutes.middleware.errors.ErrorHandlerMiddleware',)``


.. attribute:: SITE_ROOT

   This setting governs the behaviour of the Redirect class.

   Any redirect that isn't absolute will be relative to this path. E.g.
   if an application is set up at http://example.com/pyroutes/demo/ then as
   default a Redirect('/foo') will go to /pyroutes/demo/foo/. If the SITE_ROOT
   variable is set to the empty string, the redirect goes to /foo/ and if
   SITE_ROOT is set to '/bar' the redirect goes to /bar/foo/.

   **Default**: ``Detected automatically from environment``

.. attribute:: CUSTOM_BASE_TEMPLATE

   Used for custom HttpException base template.
   See the default template for an example.
   Defining only page templates and not the base template is allowed.

.. attribute:: TEMPLATE_403 = './templates/403.xml'

   Used for the rendering pages when a Http403 is raised.

.. attribute:: TEMPLATE_404 = './templates/404.xml'

   Used for the rendering pages when a Http404 is raised.

.. attribute:: TEMPLATE_500 = './templates/500.xml'

   Used for the rendering pages when a Http500 is raised.
