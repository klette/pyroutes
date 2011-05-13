Templates
=========

.. module:: pyroutes.templates


.. class:: TemplateRenderer([base_template=None, inclusion_param=None,
        template_dir=None])

   Creates a TemplateRenderer for doing single-inheritance rendering
   with XML-Template.


   Takes three parameters.

   - ``base_template``: The base template. Usually with the html headers, css, etc.
   - ``inclusion_param``: The <t:id=".."/> id which will be replaced with the content of the child template.
   - ``template_dir``: Override the ``TEMPLATE_DIR`` setting from pyroutes.settings.



.. method:: render(template, data)

   Renders a template and returns the result as a string.
   Takes two parameters, the child template to be rendered,
   and the data passed to the templates.
