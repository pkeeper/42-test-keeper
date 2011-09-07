from django.test import TestCase
from django.contrib.auth.models import User

class AdminTest(TestCase):


    def test_default_pass(self):
        admin = User(username='admin')
        self.assertIsNotNone(admin)
        self.assertTrue(admin.check_password('admin'))
