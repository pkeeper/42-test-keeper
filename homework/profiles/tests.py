from django.test import TestCase
from models import Profile, ContactField



class ProfileTest(TestCase):

    def setUp(self):
        self.profile = Profile.objects.get(pk=1)

    def test_profile_model(self):
        self.assertEqual(self.profile.name, 'Artem')
        self.assertEqual(self.profile.surname, 'Melanich')
        self.assertEqual(self.profile.bio, 'Some bio here')

    def test_contacts(self):
        contacts = ContactField.objects.filter(owner=self.profile)
        self.assertEqual(contacts.count(), 4)
        self.assertTrue(contacts.get(uid='288877528',
                                     type='icq'))
        self.assertTrue(contacts.get(uid='pkeeper@jabber.com.ua',
                                     type='jabber'))
        self.assertTrue(contacts.get(uid='pensivekeeper@gmail.com',
                                     type='jabber'))
        self.assertTrue(contacts.get(uid='pkeeper.shark@mail.ru',
                                     type='email'))

    def test_rendering(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
