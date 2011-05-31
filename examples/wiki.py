#!/usr/bin/env python
# encoding: utf-8

"""
Small wiki example using pyroutes.
"""

from pyroutes import route, application, utils
from pyroutes.http.response import Response, Redirect
from pyroutes.template import TemplateRenderer

renderer = TemplateRenderer("templates/base.xml")
nodes = {}

@route('/')
def main(request, page='index'):
    return Redirect('/show/%s' % page)

@route('/edit')
def edit(request, node='index'):
    if 'new_node_data' in request.POST:
        nodes[node] = request.POST['new_node_data']
        return Redirect('/show/%s' % node)

    template_data = {
        # XML-Template will remove the textarea node if None
        '#edit_contents': nodes.get(node, ''),
        '#edit_form/action': '/edit/%s' % node,
    }
    return Response(renderer.render("templates/edit.xml", template_data),
            status_code=404)

@route('/show')
def show(request, node='index'):
    node_contents = nodes.get(node)

    if node_contents is None:
        return Redirect("/edit/%s" % node)

    template_data = {
        '#view_contents': node_contents,
        '#edit_link/href': '/edit/%s' % node
    }
    return Response(renderer.render("templates/show.xml", template_data))

if __name__ == '__main__':
    route('/media')(utils.fileserver)
    utils.devserver(application)
