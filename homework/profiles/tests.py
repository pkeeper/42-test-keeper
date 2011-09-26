import datetime
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from models import Profile, ContactField
from forms import ProfileForm, ContactsFormSet


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

        CFormSet = modelformset_factory(ContactField, extra=2,
                                        formset=ContactsFormSet,
                                        can_delete=True, exclude=('owner',))
        contact_forms = CFormSet(profile=self.profile)
        self.assertContains(self.response, contact_forms.management_form,
                            count=1)
        self.assertContains(self.response, contact_forms.as_p(), count=1)

    def test_change(self):
        self.c.login(username='admin', password='admin')
        data = {
                u'name': [u'Artem-test'],
                u'surname': [u'Melanich-test'],
                u'birthdate': [u'1988-09-25'],
                u'bio': [u'Multiline-test'],
                u'form-0-id': [u'1'],
                u'form-0-contact_type': [u'Jabber'],
                u'form-0-uid': [u'test@mail.ru'],
                u'form-1-id': [u'2'],
                u'form-1-uid': [u'22222222'],
                u'form-1-contact_type': [u'ICQ'],
                u'form-2-id': [u'3'],
                u'form-2-DELETE': [u'on'],
                u'form-3-id': [u'4'],
                u'form-3-DELETE': [u'on'],
                u'form-4-id': [u'5'],
                u'form-4-DELETE': [u'on'],
                u'form-TOTAL_FORMS': [u'7'],
                u'form-INITIAL_FORMS': [u'5'],
                u'form-MAX_NUM_FORMS': [u''], }
        self.assertEqual(self.c.post(reverse('edit_profile'),
                                     data).status_code, 200)
        self.profile = Profile.objects.get(pk=1)
        queryset = ContactField.objects.filter(owner=self.profile)\
                                                    .order_by('pk')
        self.assertEqual(self.profile.name, 'Artem-test')
        self.assertEqual(self.profile.surname, 'Melanich-test')
        self.assertEqual(self.profile.bio, 'Multiline-test')
        self.assertEqual(queryset.count(), 2)
        self.assertEqual(queryset.get(pk=1).uid, 'test@mail.ru')
        self.assertEqual(queryset.get(pk=1).contact_type, 'Jabber')
        self.assertEqual(queryset.get(pk=2).uid, '22222222')

    def test_validation(self):
        self.c.login(username='admin', password='admin')
        data = {
                u'name': [u''], # Empty
                u'surname': [u''], # Empty
                u'birthdate': [u'notDate'],
                u'bio': [u''], # Empty
                u'form-0-id': [u'1'],
                u'form-0-contact_type': [u'ICQ'],
                u'form-0-uid': [u'test@mail.ru'],
                u'form-1-id': [u'2'],
                u'form-1-uid': [u'22222222'],
                u'form-1-contact_type': [u'Jabber'],
                u'form-2-id': [u'3'],
                u'form-2-contact_type': [u'Email'],
                u'form-2-uid': [u'notEmail'],
                u'form-3-id': [u'4'],
                u'form-3-contact_type': [u'Other contacts'],
                u'form-3-uid': [u''], # Empty
                u'form-TOTAL_FORMS': [u'6'],
                u'form-INITIAL_FORMS': [u'2'],
                u'form-MAX_NUM_FORMS': [u''], }
        response = self.c.post(reverse('edit_profile'), data)
        self.assertContains(response, '<li>This field is required.</li>',
                            count=4)
        self.assertContains(response, '<li>ICQ number is not valid.</li>',
                            count=1)
        self.assertContains(response, '<li>Jabber is not valid.</li>', count=1)
        self.assertContains(response, '<li>Email is not valid.</li>', count=1)

