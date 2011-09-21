import datetime
from django.test import TestCase
from django.core.urlresolvers import reverse
from models import Profile, ContactField


class ProfileTest(TestCase):

    def setUp(self):
        self.profile = Profile.objects.get(pk=1)

        contact_list = ContactField.objects.filter(owner=self.profile)

        self.contacts = contact_list.exclude(contact_type='Other contacts')
        self.other_cont = contact_list.filter(contact_type='Other contacts')[0]

        self.response = self.client.get(reverse('show_profile'))

    def test_profile_model(self):
        self.assertEqual(self.profile.name, 'Artem')
        self.assertEqual(self.profile.surname, 'Melanich')
        self.assertEqual(self.profile.bio, 'Multiline')
        self.assertEqual(self.profile.birthdate, datetime.date(
                                                               year=1988,
                                                               month=9,
                                                               day=15))

    def test_contacts(self):
        self.assertEqual(self.contacts.count(), 4)
        self.assertTrue(self.contacts.get(uid='288877528',
                                     contact_type='ICQ'))
        self.assertTrue(self.contacts.get(uid='pkeeper@jabber.com.ua',
                                     contact_type='Jabber'))
        self.assertTrue(self.contacts.get(uid='pensivekeeper@gmail.com',
                                     contact_type='Jabber'))
        self.assertTrue(self.contacts.get(uid='pkeeper.shark@mail.ru',
                                     contact_type='Email'))
        self.assertTrue(self.other_cont)

    def test_profile_rendering(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, self.profile.name, count=1)
        self.assertContains(self.response, self.profile.surname, count=1)
        self.assertContains(self.response, 'Sept. 15, 1988', count=1)
        self.assertContains(self.response, self.profile.bio)

    def test_profile_contacts_rendering(self):
        for c in self.contacts:
            c_rendered_html = '<p>' + c.contact_type + ': ' + c.uid + '</p>'
            self.assertContains(self.response, c_rendered_html, 1)
        self.assertContains(self.response, self.other_cont.uid)
