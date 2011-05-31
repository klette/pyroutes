# encoding: utf-8

# DEBUG shows more debug info for HTTP 500
DEBUG = True

# SECRET_KEY is used for encrypting cookie hashes. Should be set to something
# secret :)
SECRET_KEY = 'cKXOat[84t-VE5+e5ioRb]B4Q6*ve:aH'

# This setting is always detected by the dispatcher. Override it to make all
# relative redirects relative to this path. e.g. SITE_ROOT = '' makes all
# redirects «absolute». It also makes cookies set for the entire site.
#SITE_ROOT = '/projects/wiki'

# Path to media files. Used by development media server in contrib.
#DEV_MEDIA_BASE = '.'

# Used for custom HttpException.
# Passed variables are request and title.
# Defining only page templates and not base template is allowed.
#CUSTOM_BASE_TEMPLATE = './templates/pyroutes/base_override.xml'
#TEMPLATE_403 = './templates/403.xml'
#TEMPLATE_404 = './templates/404.xml'
#TEMPLATE_500 = './templates/500.xml'
