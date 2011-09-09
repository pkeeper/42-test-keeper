from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from models import RequestEntry


class RequestsAppTest(TestCase):
    
    def middleware_test(self):
        
        c = Client()
        response = c.get('/', 
                         {'name': 'fred', 'age': 7},
                         HTTP_X_REQUESTED_WITH='TestRequest')
        self.assertEqual(response.status_code, 200)
        req = RequestEntry.objects.order_by('-created_at')[0]
        self.assertEqual(req.path, '/')
        self.assertEqual(req.method, 'GET')
        self.assertEqual(req.params, {'name': 'fred', 'age': 7})
        self.assertIn(req.header, {'HTTP_X_REQUESTED_WITH':'TestRequest'})
        
    def request_view_test(self):
        c = Client()
