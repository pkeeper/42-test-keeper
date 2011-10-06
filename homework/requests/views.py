from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import RequestEntry
from forms import RequestPriorityForm


def requests_list(request, template_name='request-list.html'):
    if request.method == 'POST':
        postdata = request.POST.copy()
        r = get_object_or_404(RequestEntry, pk=postdata['pk'])
        form = RequestPriorityForm(postdata, instance=r)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('requests_list'))
    # Continue if GET or form not valid
    requests = RequestEntry.objects.order_by('-priority', '-created_at')[:10]
    for r in requests:
        r.form = RequestPriorityForm(instance=r)
    return render_to_response(template_name,
                              {'requests': requests},
                              context_instance=RequestContext(request))
