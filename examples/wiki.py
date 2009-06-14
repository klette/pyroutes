#!/usr/bin/env python
# encoding: utf-8

"""
Small wiki example using pyroutes
"""

from __future__ import with_statement

from wsgiref.simple_server import make_server
import hashlib
import memcache

from pyroutes import route, application
from pyroutes.http import Response, Redirect
import pyroutes.template
from pyroutes.template import TemplateRenderer

cache = memcache.Client(['localhost:11211'])
renderer = TemplateRenderer("templates/base.xml")

@route('/')
def main(environ, data):
    return Response("redirect", [('Location', '/show/index')], "302 See Other")

@route('/edit')
def edit(environ, data):
    node = environ['PATH_INFO'][6:]
    
    if 'new_node_data' in data:
        cache.set(node, data['new_node_data'])
        return Redirect('/show/%s' % node)
    
    template_data = {
        '#edit_contents': cache.get(node) or '' # XML-Template will remove the textarea node if None
        '#edit_form/action': '/edit/%s' % node,
    }
    return Response(renderer.render("templates/edit.xml", template_data), status_code="404 Not Found")

@route('/show')
def show(environ, data):
    node = environ['PATH_INFO'][6:]
    node_contents = cache.get(node)
    
    if not node_contents:
        return Redirect("/edit/%s" % node)
    
    template_data = {
    	'#view_contents': node_contents,
    	'#edit_link/href': '/edit/%s' % node
    }
    return Response(renderer.render("templates/show.xml", template_data))
    

if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print "Serving on port 8000..."
    httpd.serve_forever()


