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
