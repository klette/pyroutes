import datetime
import mimetypes
import os
import time

import pyroutes
from pyroutes.template import TemplateRenderer
from pyroutes.http import Response, Redirect, Http403, Http404
from wsgiref.util import FileWrapper

def fileserver(environ, data):
    """
    Simple file server for development servers. Not for use in production
    environments. Usage:

    media_server = route('/media')(pyroutes.contrib.util.fileserver)

    That will add the fileserver to the route /media. If DEV_MEDIA_BASE is
    defined in settings, host files from this folder. Otherwise, use current
    working directory.

    NOTE: DEV_MEDIA_BASE and route path is concatenated, i.e. if you use
    '/srv/media' for as the media base, and map the route to '/files', all
    files will be looked for in '/srv/media/files'
    """

    request = environ['PATH_INFO']
    request_list = request.lstrip('/').split('/')
    if hasattr(pyroutes.settings, 'DEV_MEDIA_BASE'):
        path = os.path.join(pyroutes.settings.DEV_MEDIA_BASE, *request_list)
    else:
        path = os.path.join('.', *request_list)

    if not os.path.exists(path):
        raise Http405

    if not os.access(path, os.R_OK):
        raise Http403

    modified = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    if 'HTTP_IF_MODIFIED_SINCE' in environ:
        # This is a hack for python2.4 compat
        last_time = datetime.datetime(
            *time.strptime(
                environ.get('HTTP_IF_MODIFIED_SINCE'),
                "%a, %d %b %Y %H:%M:%S"
            )[0:6]
        )
        if last_time == modified:
            return Response(status_code='304 Not Modified')
    modified = datetime.datetime.strftime(modified, "%a, %d %b %Y %H:%M:%S")

    headers = [
        ('Last-Modified', modified),
    ]

    if os.path.isdir(path):
        if not request.endswith('/'):
            return Redirect(request + '/')

        listing = []
        files = []
        for file in sorted(os.listdir(path)):
            if os.path.isdir(os.path.join(path, file)):
                listing.append({'li': {'a': file + "/", 'a/href': file + "/"}})
            else:
                files.append({'li': {'a': file, 'a/href': file}})
        # Done to list folders before files
        listing += files

        template_data = {
            'file_list': listing,
            'title': 'Listing of %s' % request
        }

        templaterenderer = TemplateRenderer(
            pyroutes.settings.BUILTIN_BASE_TEMPLATE
        )
        return Response(
            templaterenderer.render(
                os.path.join(pyroutes.settings.BUILTIN_TEMPLATES_DIR,
                    'fileserver', 'directory_listing.xml'
                ),
                template_data
            )
        )

    contenttype = mimetypes.guess_type(path)[0] or "application/octet-stream"
    file = FileWrapper(open(path))
    size = os.path.getsize(path)

    headers.append(('Content-Type', contenttype))
    headers.append(('Content-Length', str(size)))

    return Response(file, headers=headers)

