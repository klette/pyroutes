#!/usr/bin/env python
# encoding: utf-8
"""
"""

import xmltemplate

class TemplateRenderer():
    """
    """
    
    def __init__(self, base_template=None):
        """
        """
        self.base_template = base_template
        
    def render(self, template, data, inclusion_param='contents'):
        """
        """
        if self.base_template:
            doc = xmltemplate.process_file(template, data, False)
            data[inclusion_param] = doc
            master = xmltemplate.process_file(self.base_template, data);
        else:
            master = xmltemplate.proccess_file(template, data)
        return master.toxml().encode("utf-8")
