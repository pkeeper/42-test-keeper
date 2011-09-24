from django import forms
from django.core.validators import validate_email
from django.forms.models import BaseModelFormSet
from models import Profile, ContactField


class ProfileForm(forms.ModelForm):
    """
        Form for Profile model
    """
    class Meta:
        model = Profile


class ContactsFormSet(BaseModelFormSet):

    def clean(self):
        super(ContactsFormSet, self).clean()
        """Checks that uid is valid for given contact type."""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid
            # on its own
            return
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            # Do not validate if object is deleting
            if form in self.deleted_forms:
                continue
            # Do not validate empty extra forms
            if not form.initial and not form.cleaned_data:
                continue
            uid = form.cleaned_data['uid']
            contact_type = form.cleaned_data['contact_type']
            if contact_type in ('Email', 'Jabber'):
                    try:
                        validate_email(uid)
                    except:
                        raise forms.ValidationError(uid + ' ' + contact_type +
                                                    " is not valid")
                        return False
            if contact_type == "ICQ":
                if not uid.isnumeric():
                    raise forms.ValidationError(uid +
                                                ' ICQ number is not valid')
                    return False

    def __init__(self, *args, **kwargs):
        self.queryset = ContactField.objects.filter(owner=kwargs['profile'])\
                                                   .order_by('pk')
        del kwargs['profile']
        super(BaseModelFormSet, self).__init__(*args, **kwargs)
