from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from models import RequestEntry


class RequestsAppTest(TestCase):
    
    def setUp(self):
        c = Client()
        self.responseA = c.get('/', 
                         {'name': 'fred', 'age': '7'},
                         HTTP_X_REQUESTED_WITH='TestRequest')
        self.responseB = c.get(reverse('requests_list'))
    
    def test_middleware(self):
        
        self.assertEqual(self.responseA.status_code, 200)
        req = RequestEntry.objects.order_by('-created_at')[1]
        self.assertEqual(req.path, '/')
        self.assertEqual(req.method, 'GET')
        self.assertItemsEqual(eval(req.params), {'name': 'fred', 'age': '7'})
        self.assertEqual('TestRequest', eval(req.headers)['HTTP_X_REQUESTED_WITH'])
        
    def test_request_view(self):
        
        req = RequestEntry.objects.order_by('-created_at')[:10]
        self.assertEqual(self.responseB.context['requests'].count(), 2)
        self.assertEqual(req.count(), 2)
        
        self.assertEqual(self.responseB.status_code, 200)
        self.assertEqual(self.responseB.context['requests'][0].path, reverse('requests_list'))
        
        
