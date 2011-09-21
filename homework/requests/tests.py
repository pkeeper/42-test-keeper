from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from models import RequestEntry


class RequestsAppTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_middleware(self):
        response = self.c.get('/',
                         {'name': 'fred', 'age': '7'},
                         HTTP_X_REQUESTED_WITH='TestRequest')
        self.assertEqual(response.status_code, 200)
        req = RequestEntry.objects.order_by('-created_at')[0]
        self.assertEqual(req.path, '/')
        self.assertEqual(req.method, 'GET')
        self.assertItemsEqual(eval(req.params), {'name': 'fred', 'age': '7'})
        self.assertEqual('TestRequest',
                         eval(req.headers)['HTTP_X_REQUESTED_WITH'])

    def test_request_view(self):
        # Make 12 test requests
        for i in range(1, 12):
            response = self.c.get(reverse('requests_list'))
        # Get last requests and check them
        req = RequestEntry.objects.order_by('-created_at')[:10]
        for r in req:
            self.assertContains(response, '<p>Request path: ' + r.path +
                                '</p>', count=10, status_code=200)
            self.assertContains(response, '<p>Request parameters: ' +
                                r.params + '</p>', count=10)
            self.assertContains(response,
                                '{&#39;REMOTE_ADDR&#39;: &#39;127.0.0.1&#39;}',
                                count=10)
