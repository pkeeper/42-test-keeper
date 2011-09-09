from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from models import Profile, ContactField


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
