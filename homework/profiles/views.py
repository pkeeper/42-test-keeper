from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.template import RequestContext
from models import Profile, ContactField
from forms import ProfileForm, ContactsFormSet


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
    CFormSet = modelformset_factory(ContactField, can_delete=True,
                                           formset=ContactsFormSet,
                                           extra=2, fields=('uid',
                                                            'contact_type'))

    if request.method == 'POST':
        postdata = request.POST.copy()
        profile_form = ProfileForm(postdata, instance=profile)
        contact_forms = CFormSet(postdata, profile=profile)
        if request.is_ajax:
            if not profile_form.is_valid() or not contact_forms.is_valid():
                html = profile_form.errors.as_ul()
                for f in contact_forms:
                    html += f.errors.as_ul()
                return HttpResponse('Form not valid!<br/>Errors:<br/>' + html)
        if profile_form.is_valid() and contact_forms.is_valid():
            # Save changes in forms
            profile_form.save()
            contact_forms.save()
            # Reload forms to display fresh data
            profile_form = ProfileForm(instance=profile)
            contact_forms = CFormSet(profile=profile)
    else:
        profile_form = ProfileForm(instance=profile)
        contact_forms = CFormSet(profile=profile)
    context_dict = {
                    'profile_form': profile_form,
                    'contatcs_forms': contact_forms,
                   }

    return render_to_response(template_name,
                              context_dict,
                              context_instance=RequestContext(request))
