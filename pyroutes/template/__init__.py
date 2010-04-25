#!/usr/bin/env python
# encoding: utf-8
"""
"""
import os
import xmltemplate
from pyroutes import settings

class TemplateRenderer(object):
    """
    A small wrapper for doing basic template includes with xml-template

    The constructor takes two arguments, a base template and an inclusion parameter.
    The base template must have a <t:contents /> node in it which will be replaced with
    the contents of the included template. The contents identifier can
    be overriden with the second constructor argument, `inclusion_param`.
    If None is given as the base template, the `render`-method will not try
    to do any inclusion and only render the given template.
    """

    def __init__(self, base_template=None, inclusion_param='contents', template_dir=None):
        """
        """
        self.base_template = base_template
        self.inclusion_param = inclusion_param
        if template_dir != None:
            self.template_dir = template_dir
        elif settings.TEMPLATE_DIR:
            self.template_dir = settings.TEMPLATE_DIR
        else:
            self.template_dir = ''

    def render(self, template, data):
        """
        """
        if self.base_template:
            doc = xmltemplate.process_file(os.path.join(self.template_dir, template), data, False)
            data[self.inclusion_param] = doc
            master = xmltemplate.process_file(os.path.join(self.template_dir, self.base_template), data);
        else:
            master = xmltemplate.process_file(os.path.join(self.template_dir, template), data)
        return master.toxml().encode("utf-8")
