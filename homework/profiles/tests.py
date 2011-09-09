import datetime
from django.test import TestCase
from models import Profile, ContactField


class ProfileTest(TestCase):

    def setUp(self):
        self.profile = Profile.objects.get(pk=1)

    def test_profile_model(self):
        self.assertEqual(self.profile.name, 'Artem')
        self.assertEqual(self.profile.surname, 'Melanich')
        self.assertEqual(self.profile.bio, 'Multiline')
        #self.assertEqual(self.profile.birthdate, datetime.date(
        #                                                       year=1988,
        #                                                       month=9,
        #                                                       day=15))

    def test_contacts(self):
        contacts = ContactField.objects.filter(owner=self.profile)
        self.assertEqual(contacts.count(), 5)
        self.assertTrue(contacts.get(uid='288877528',
                                     contact_type='ICQ'))
        self.assertTrue(contacts.get(uid='pkeeper@jabber.com.ua',
                                     contact_type='Jabber'))
        self.assertTrue(contacts.get(uid='pensivekeeper@gmail.com',
                                     contact_type='Jabber'))
        self.assertTrue(contacts.get(uid='pkeeper.shark@mail.ru',
                                     contact_type='Email'))
        self.assertTrue(contacts.get(uid='Multiline',
                                     contact_type='Other contacts'))

    def test_rendering(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
