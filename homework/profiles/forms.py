from django import forms
from django.utils.safestring import mark_safe
from models import Profile


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
        widgets = {
            'birthdate': CustomDateWidget(),
        }
