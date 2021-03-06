"""
Module pyroutes.settings
Used for importing settings, and defining default settings

Override per project settings in pyroutes_settings.py in
your project folder
"""

import os

# Default template dir, relative to this imported __file__
BUILTIN_TEMPLATES_DIR = os.path.join(
    os.path.dirname(__file__),
    'default_templates'
)
BUILTIN_BASE_TEMPLATE = 'base.xml'

# This should have an override for development servers
DEBUG = False

# For setting the default content type
DEFAULT_CONTENT_TYPE = 'text/html; charset=utf-8'

# Secret key for crypto. SET THIS in pyroutes_settings!
SECRET_KEY = None

# Location for templates. Used by TemplateRenderer
TEMPLATE_DIR = None # /foo/bar/templates/

# Middleware
MIDDLEWARE = (
    'pyroutes.middleware.errors.NotFoundMiddleware',
    #'pyroutes.middleware.appendslash.AppendSlashes',
    'pyroutes.middleware.responsify.Responsify',
    'pyroutes.middleware.errors.ErrorHandlerMiddleware',
)

# Attempt to get custom settings. Not obligatory.
try:
    from pyroutes_settings import *
except ImportError:
    pass
