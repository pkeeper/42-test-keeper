import datetime
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from models import Profile, ContactField
from forms import ProfileForm, ContactsFormSet


class ProfileShowTest(TestCase):

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
                                        can_delete=True, fields=('uid',
                                                            'contact_type'))
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

class DateWidgetTest(TestCase):
    fixtures = ['admin_data.json', ]

    def test_widget_output(self):
        out = '''<script>
            $(function() {
                $("#id_'''
        out2 = '''").datepicker({ dateFormat: 'yy-mm-dd'});
            });
            </script>'''
        c = Client()
        self.assertTrue(c.login(username='admin', password='admin'))
        response = c.get(reverse('edit_profile'))
        self.assertContains(response, out)
        self.assertContains(response, out2)
