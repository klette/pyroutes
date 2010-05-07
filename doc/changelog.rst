Changelog
=========

Release 0.3.0
-------------

- Added support for autopopulating handler method with data from the URL.
- Added middleware support
- New and improved documentation
- Lots of cleanups on the code.


Release 0.2.2
-------------

- Fixed bug where setting the TEMPLATE_DIR-option in ``pyroutes_settings.py``
  would cause the default 404,403 and 400 error pages to not work.
- Fix bug where pyroutes would add two content-type headers to responses. (Thanks to Dalton Barreto)
- Fixed IF_MODIFIED_SINCE handling in utils.fileserver on windows.

Release 0.2.1
-------------

- Reduce setup.py dependencies to only distutils.
- Fix packaging of default templates
- Fix pypi-package complaining about README file missing.
- Fix unstable cookie handling in some cornercases.

Release 0.2.0
-------------

- New Request object included to every route. *Backward incompatible*
- New cookie handling framework
- Automatic HTTP-status code lookups in Response-objects.
- Project settings
- Better debug-pages when DEBUG=True in settings.
- Development fileserver
- Development autoreloader

