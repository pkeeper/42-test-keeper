from django import forms
from models import Profile, ContactField


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        
class ContactFieldForm(forms.ModelForm):
    class Meta:
        model = ContactField
        exclude = ('owner',)