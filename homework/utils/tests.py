from StringIO import StringIO

from django.test import TestCase
from django.test.client import Client
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.management import call_command


class RequestsAppTest(TestCase):

    def setUp(self):
        c = Client()
        self.response = c.get('/')

    def test_context_processor(self):

        self.assertEqual(self.response.status_code, 200)
        self.assertIs(self.response.context['SETTINGS'], settings)


class AdmEditTagTest(TestCase):

    def test_tag_render(self):
        obj = User.objects.get(pk=1)
        t = template.Template('{% load utils_tags %}{% edit_link obj %}')
        c = template.Context({'obj': obj})
        rendered = t.render(c)
        content_type = ContentType.objects.get_for_model(obj.__class__)
        link = reverse("admin:%s_%s_change" %
                       (content_type.app_label, content_type.model),
                       args=(obj.id,))
        self.assertEqual(rendered, link)


class ModelscountCommandTest(TestCase):

    def setUp(self):
        self.out = StringIO()
        self.err_out = StringIO()

    def test_command(self):
        """ Test default output."""
        call_command("modelscount", stdout=self.out, stderr=self.err_out,
                     database='default')
        ctypes = ContentType.objects.all()
        for c in ctypes:
            self.assertIn(c.model, self.out.getvalue())
            self.assertIn(c.model, self.err_out.getvalue())

    def test_command_args(self):
        """ Test output for app list."""
        call_command("modelscount", 'auth', 'sites', stdout=self.out,
                     stderr=self.err_out, database='default')
        ctypes = ContentType.objects.all()
        cfilt = ctypes.exclude(app_label='auth').exclude(app_label='sites')
        for c in cfilt:
            self.assertNotIn(c.model, self.out.getvalue())
            self.assertNotIn(c.model, self.err_out.getvalue())
        cfilt = ctypes.filter(app_label='auth').filter(app_label='sites')
        for c in cfilt:
            self.assertIn(c.model, self.out.getvalue())
            self.assertIn(c.model, self.err_out.getvalue())

    def test_multidb(self):
        try:
            call_command("modelscount", stdout=self.out, stderr=self.err_out,
                         database='wrongdb')
            error = True
        except:
            error = False
        if error:
            self.fail("No error msg on wrong db")
        self.assertIn("Error: The connection wrongdb doesn't exist."
                      " Wrong database alias?", self.err_out.getvalue())
