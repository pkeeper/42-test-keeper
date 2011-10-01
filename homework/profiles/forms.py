from django import forms
from django.utils.safestring import mark_safe
from django.core.validators import validate_email
from django.forms.models import BaseModelFormSet
from django.forms.util import ErrorList
from models import Profile, ContactField


class CustomDateWidget(forms.DateInput):
    """
        Widget that adds calendar to DateField
        Requires jQuery
    """
    class Media:
        css = {
            'all': ('css/ui-lightness/jquery-ui-1.8.16.custom.css',)}
        js = ('js/jquery-ui-1.8.16.custom.min.js',)

    def render(self, name, value, attrs=None):
        rendered = super(CustomDateWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script>
            $(function() {
                $("#id_%(name)s").datepicker({ dateFormat: 'yy-mm-dd'});
            });
            </script>''' % {'name': name})


class ProfileForm(forms.ModelForm):
    """
        Form for Profile model
    """
    class Meta:
        model = Profile
        fields = ('bio', 'birthdate', 'surname', 'name')
        widgets = {
            'birthdate': CustomDateWidget(),
        }


class ContactsFormSet(BaseModelFormSet):

    def clean(self):
        super(ContactsFormSet, self).clean()
        """Checks that uid is valid for given contact type."""
        form_is_valid = True
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            # Do not validate if object is deleting
            if getattr(self, 'deleted_forms', False):
                if form in self.deleted_forms:
                    continue
            # Do not validate empty extra forms
            if not getattr(form, 'cleaned_data', False):
                continue
            uid = form.cleaned_data['uid']
            contact_type = form.cleaned_data['contact_type']
            if contact_type in ('Email', 'Jabber'):
                    try:
                        validate_email(uid)
                    except:
                        if not getattr(form._errors, 'contact_type', False):
                            form._errors['contact_type'] = ErrorList()
                        form._errors['contact_type'].append(contact_type +
                                                            " is not valid.")
                        form_is_valid = False
            if contact_type == "ICQ":
                if not uid.isnumeric():
                    if not getattr(form._errors, 'contact_type', False):
                        form._errors['contact_type'] = ErrorList()
                    form._errors['contact_type']\
                                            .append('ICQ number is not valid.')
                    form_is_valid = False
        return form_is_valid

    def __init__(self, *args, **kwargs):
        queryset = ContactField.objects.filter(owner=kwargs['profile'])\
                                                   .order_by('-pk')
        if queryset is not None:
            self.queryset = queryset
        del kwargs['profile']
        super(BaseModelFormSet, self).__init__(*args, **kwargs)
