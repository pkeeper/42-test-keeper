import datetime
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from models import Profile, ContactField
from forms import ProfileForm


class ProfileShowTest(TestCase):

    def setUp(self):
        self.profile = Profile.objects.get(pk=1)

    def test_profile_model(self):
        self.assertEqual(self.profile.name, 'Artem')
        self.assertEqual(self.profile.surname, 'Melanich')
        self.assertEqual(self.profile.bio, 'Multiline')
        self.assertEqual(self.profile.birthdate, datetime.date(
                                                               year=1988,
                                                               month=9,
                                                               day=15))

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


class ProfileEditTest(TestCase):
    fixtures = ['admin_data.json', ]

    def setUp(self):
        self.profile = Profile.objects.get(pk=1)
        self.c = Client()

    def test_edit_useronly(self):
        self.response = self.c.get(reverse('edit_profile'))
        self.assertEqual(self.response.status_code, 302)
        self.assertTrue(self.c.login(username='admin', password='admin'))
        self.response = self.c.get(reverse('edit_profile'))
        self.assertEqual(self.response.status_code, 200)

    def test_edit_render(self):
        form = ProfileForm(instance=self.profile)
        self.assertTrue(self.c.login(username='admin', password='admin'))
        self.response = self.c.get(reverse('edit_profile'))
        self.assertContains(self.response, form.as_p(), count=1,
                            status_code=200)

        contact_list = ContactField.objects.filter(owner=self.profile)
        ContactsFormSet = modelformset_factory(ContactField, extra=2,
                                               exclude=('owner',))
        contact_forms = ContactsFormSet(queryset=contact_list)
        self.assertContains(self.response, contact_forms.management_form,
                            count=1)
        self.assertContains(self.response, contact_forms.as_p(), count=1)
