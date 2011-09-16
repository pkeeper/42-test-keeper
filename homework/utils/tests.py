from django.test import TestCase
from django.test.client import Client

from django.conf import settings


class RequestsAppTest(TestCase):

    def setUp(self):
        c = Client()
        self.response = c.get('/')

    def test_context_processor(self):

        self.assertEqual(self.response.status_code, 200)
        self.assertIs(self.response.context['SETTINGS'], settings)
