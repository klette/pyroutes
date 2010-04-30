import datetime
import mimetypes
import os
import posixpath
import time

os.path = posixpath

import pyroutes
from pyroutes import settings
from pyroutes.template import TemplateRenderer
from pyroutes.http.response import Response, Redirect, Http403, Http404
from pyroutes.contrib import autoreload

from wsgiref.simple_server import make_server
from wsgiref.util import FileWrapper

def devserver(application, port=8001, address='0.0.0.0', auto_reload=True):
    """
    Simple development server for rapid development. Use to create a simple web
    server. For testing purposes only. Has no builting handling of file
    serving, use fileserver in this class. Typical usage::

        from pyroutes import route, application, utils
        #<define routes>
        if __name__ == '__main__':
            utils.devserver(application)

    This starts a server listening on all interfaces, port 8001. It
    automatically reloads modified files.
    """

    def server_thread():
        httpd = make_server(address, port, application)
        print "Starting server on %s port %d..." % (address, port)
        httpd.serve_forever()
    if auto_reload:
        autoreload.main(server_thread)
    else:
        server_thread()

def fileserver(request):
    """
    Simple file server for development servers. Not for use in production
    environments. Typical usage::

        from pyroutes import route, utils
        route('/media')(utils.fileserver)

    That will add the fileserver to the route /media. If DEV_MEDIA_BASE is
    defined in settings, host files from this folder. Otherwise, use current
    working directory.

    .. note::
        DEV_MEDIA_BASE and route path is concatenated, i.e. if you use
        '/srv/media' for as the media base, and map the route to '/files', all
        files will be looked for in '/srv/media/files'
    """

    path = request.ENV['PATH_INFO']
    path_list = path.lstrip('/').split('/')

    # Do not expose entire file system
    if '..' in path_list:
        raise Http404

    if hasattr(settings, 'DEV_MEDIA_BASE'):
        path = os.path.join(settings.DEV_MEDIA_BASE, *path_list)
    else:
        path = os.path.join('.', *path_list)

    if not os.path.exists(path):
        raise Http404

    if not os.access(path, os.R_OK):
        raise Http403

    modified = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    if 'HTTP_IF_MODIFIED_SINCE' in request.ENV:
        modified = datetime.datetime.strftime(modified, "%a, %d %b %Y %H:%M:%S")
        if request.ENV.get('HTTP_IF_MODIFIED_SINCE') == modified:
            return Response(status_code='304 Not Modified',
                    default_content_header=False)
    modified = datetime.datetime.strftime(modified, "%a, %d %b %Y %H:%M:%S")

    headers = [
        ('Last-Modified', modified),
    ]

    if os.path.isdir(path):
        if not path.endswith('/'):
            return Redirect(path + '/')

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
            'title': 'Listing of %s' % path
        }

        templaterenderer = TemplateRenderer(
            settings.BUILTIN_BASE_TEMPLATE,
            template_dir=settings.BUILTIN_TEMPLATES_DIR
        )
        return Response(
            templaterenderer.render(
                os.path.join('fileserver', 'directory_listing.xml'),
                template_data
            ),
            headers
        )

    contenttype = mimetypes.guess_type(path)[0] or "application/octet-stream"
    file = FileWrapper(open(path))
    size = os.path.getsize(path)

    headers.append(('Content-Type', contenttype))
    headers.append(('Content-Length', str(size)))

    return Response(file, headers=headers)
