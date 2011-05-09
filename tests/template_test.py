import unittest

from pyroutes import template, settings

class TestXMLTemplates(unittest.TestCase):

    template_dir = 'examples/templates'
    base_template = 'base.xml'
    child_template = 'show.xml'
    test_string = 'STRINGTOLOOKFOR'

    def setUp(self):
        pass

    def _render_template(self, template, data):
        output = self.renderer.render(template, data)
        self.assertTrue(self.test_string in output)

class TestsWithBaseTemplate(TestXMLTemplates):

    def setUp(self):
        self.renderer = template.TemplateRenderer(self.base_template,
                template_dir=self.template_dir)

    def test_render_with_child(self):
        self._render_template(self.child_template,
                {'#view_contents': self.test_string})

    def test_render_id_attribute(self):
        self._render_template(self.child_template,
                {'#view_contents/class': self.test_string})

class TestsWithoutBaseTemplate(TestXMLTemplates):

    def setUp(self):
        self.renderer = template.TemplateRenderer(
                template_dir=self.template_dir)

    def test_render_simple_template(self):
        self._render_template(self.base_template,
                {'contents': self.test_string})

class TestsWithBaseAndDirFromSettings(TestsWithBaseTemplate):

    def setUp(self):
        settings.TEMPLATE_DIR = self.template_dir
        self.renderer = template.TemplateRenderer(self.base_template)

    def tearDown(self):
        settings.TEMPLATE_DIR = None
