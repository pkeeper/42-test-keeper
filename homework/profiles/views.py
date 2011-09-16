from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.template import RequestContext
from models import Profile, ContactField
from forms import ProfileForm, ContactFieldForm


def show_profile(request, template_name="home.html"):
    profile = get_object_or_404(Profile, pk=1)
    contact_list = ContactField.objects.filter(owner=profile)
    contacts = contact_list.exclude(contact_type='Other contacts')
    other_contacts = contact_list.filter(contact_type='Other contacts')

    context_dict = {
                    'profile': profile,
                    'contacts': contacts,
                    'other_contacts': other_contacts,
                   }

    return render_to_response(template_name,
                              context_dict,
                              context_instance=RequestContext(request))

@login_required
def edit_profile(request, template_name="profile_edit.html"):
    profile = get_object_or_404(Profile, pk=1)
    contact_list = ContactField.objects.filter(owner=profile)
    ContactsFormSet = modelformset_factory(ContactField, extra=2, exclude=('owner',))

    if request.method == 'POST':
        postdata = request.POST.copy()
        profile_form = ProfileForm(postdata, instance=profile)
        contact_forms = ContactsFormSet(postdata, queryset=contact_list)
        if profile_form.is_valid() and contact_forms.is_valid() :
            profile_form.save()
            contact_forms.save()
    else:
        profile_form = ProfileForm(instance=profile)
        contact_forms = ContactsFormSet(queryset=contact_list)
    context_dict = {
                    'profile_form': profile_form,
                    'contatcs_forms': contact_forms,
#                    'other_contacts': other_contacts,
                   }

    return render_to_response(template_name,
                              context_dict,
                              context_instance=RequestContext(request))