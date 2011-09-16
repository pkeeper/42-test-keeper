from django.test import TestCase
from django.test.client import Client


class RequestsAppTest(TestCase):

    def setUp(self):
        c = Client()
        self.response = c.get('/')

    def test_context_processor(self):

        self.assertEqual(self.response.status_code, 200)
        from django.conf import settings
        self.assertItemsEqual(self.response.context['settings'], settings)
        
