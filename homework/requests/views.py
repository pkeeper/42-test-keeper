from django.shortcuts import render_to_response
from django.template import RequestContext
from models import RequestEntry


def requests_list(request, template_name='request-list.html'):
    requests = RequestEntry.objects.order_by('-priority', '-created_at')[:10]
    return render_to_response(template_name,
                              {'requests': requests},
                              context_instance=RequestContext(request))
