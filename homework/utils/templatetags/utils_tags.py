from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.simple_tag
def edit_link(obj):
    content_type = ContentType.objects.get_for_model(obj.__class__)
    return '''<a href="''' + reverse("admin:%s_%s_change" %
                                   (content_type.app_label, content_type.model),
                                   args=(obj.id,)) + '''">(admin)</a>'''
