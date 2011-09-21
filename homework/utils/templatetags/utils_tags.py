from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.simple_tag
def edit_link(obj):
    """
       Renders admin link for object (instance of model)
       Usage:
           {% load utils_tags %}
           {% edit_link your_model_instance %}
    """

    content_type = ContentType.objects.get_for_model(obj.__class__)
    return reverse("admin:%s_%s_change" %
                   (content_type.app_label, content_type.model),
                   args=(obj.id,))
