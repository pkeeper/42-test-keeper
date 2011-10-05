from django.test import TestCase
from django.contrib.sites.models import Site
from models import SignalLog


class SignalLoggerTest(TestCase):

    def setUp(self):
        # Test with sites framework (it's always available)
        self.test_obj = Site(domain='example.com', name='test')
        self.test_obj.save()

        self.log = SignalLog.objects

        # Count objects after syncdb
        self.first_count = self.log.count()

    def test_log_on_creation(self):

        latest_log = self.log.latest('created_at')
        self.assertEqual(latest_log.action, 'Create')
        self.assertEqual(latest_log.content_type.app_label, 'sites')
        self.assertEqual(latest_log.content_type.model, 'site')

    def test_log_on_edit(self):
        test_obj = Site.objects.get(name='test')
        test_obj.name = 'test_test'
        test_obj.save()

        latest_log = SignalLog.objects.order_by('-created_at')[0]
        self.assertEqual(latest_log.action, 'Change')
        self.assertEqual(latest_log.content_type.app_label, 'sites')
        self.assertEqual(latest_log.content_type.model, 'site')

    def test_log_on_delete(self):
        self.test_obj.delete()

        latest_log = self.log.latest('created_at')
        self.assertEqual(latest_log.action, 'Delete')
        self.assertEqual(latest_log.content_type.app_label, 'sites')
        self.assertEqual(latest_log.content_type.model, 'site')
