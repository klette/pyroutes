.. _ref-pyroutes-settings

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
   You should always append to this list if enabling more middleware,
   as the defaults should always be there.

   You can read more about middleware here :ref:`middleware`.

   **Default**: ``['pyroutes.middleware.errors.NotFoundMiddleware',
   'pyroutes.middleware.errors.ErrorHandlerMiddleware',]``
