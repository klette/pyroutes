#!/usr/bin/env python
# encoding: utf-8

"""
Small wiki example using pyroutes
"""

from __future__ import with_statement

from wsgiref.simple_server import make_server
import hashlib

from pyroutes import route, application
from pyroutes.http import Response, Redirect
import pyroutes.template
from pyroutes.template import TemplateRenderer

DATA_DIR = '/tmp/'

renderer = TemplateRenderer("templates/base.xml")

def read_node(node_name):
    """
    Calculates the sha1-sum of a node name, and
    reads the data from disk. If the file does not
    exists, it returns None
    """
    node_hash = hashlib.sha1(node_name).hexdigest()
    try:
        with open(DATA_DIR  + node_hash, 'r') as f:
            node_data = f.read()
    except IOError:
        node_data = ""
    return node_data

def write_node(node_name, contents):
    """
    Calculates the sha1-sum of the node name and
    write the given contents to that file
    """
    node_hash = hashlib.sha1(node_name).hexdigest()
    with open(DATA_DIR + node_hash, 'wb') as f:
        f.write(contents)

@route('/')
def main(environ, data):
    return Response("redirect", [('Location', '/show/index')], "302 See Other")

@route('/')
def main2(environ, data):
    return Response("redirect", [('Location', '/show/index')], "302 See Other")

@route('/edit')
def edit(environ, data):
    node = environ['PATH_INFO'][6:]
    
    if 'new_node_data' in data:
        write_node(node, data['new_node_data'])
        return Redirect('/show/%s' % node)
    
    template_data = {
        '#edit_contents': read_node(node),
        '#edit_form/action': '/edit/%s' % node,
    }
    return Response(renderer.render("templates/edit.xml", template_data), status_code="404 Not Found")

@route('/show')
def show(environ, data):
    node = environ['PATH_INFO'][6:]
    node_contents = read_node(node)
    
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


