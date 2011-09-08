from django.shortcuts import get_object_or_404, render_to_response
from profiles.models import Profile, ContactField

def show_profile(request, template_name="home.html"):
    profile = get_object_or_404(Profile,pk=1)
    contacts = ContactField.objects.filter(owner=profile)
    return render_to_response(template_name,{'profile':profile,
                                             'contacts':contacts})