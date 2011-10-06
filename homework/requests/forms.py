from django import forms
from models import RequestEntry



class RequestPriorityForm(forms.ModelForm):
    """
        Form for Profile model
    """
    class Meta:
        model = RequestEntry
        fields = ('priority',)
