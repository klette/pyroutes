import os

"""Used for importing settings, and defining default settings"""

# Default template dir, relative to this imported __file__
BUILTIN_TEMPLATES_DIR = os.path.join(
    os.path.dirname(__file__),
    'default_templates'
)
BUILTIN_BASE_TEMPLATE = os.path.join(BUILTIN_TEMPLATES_DIR, 'base.xml')

# This should have an override for development servers
DEBUG = False

# For setting the default content type
DEFAULT_CONTENT_TYPE = 'text/html; charset=utf8'

# Attempt to get custom settings. Not obligatory.
try:
    from pyroutes_settings import *
except ImportError:
    pass
