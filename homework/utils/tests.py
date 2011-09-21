from django.test import TestCase
from django.test.client import Client
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.management import call_command
from management.commands.modelscount import print_apps


class RequestsAppTest(TestCase):

    def setUp(self):
        c = Client()
        self.response = c.get('/')

    def test_context_processor(self):

        self.assertEqual(self.response.status_code, 200)
        self.assertIs(self.response.context['SETTINGS'], settings)


class AdmEditTagTest(TestCase):

    fixtures = ['admin_data.json', ]

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

    def test_command(self):
        """ Test my custom command."""

        out, err_out = print_apps()
        self.assertTrue(out)
        self.assertTrue(err_out)
