from django import template
from django.conf import settings
from whats_fresh.whats_fresh_api.models import Theme


register = template.Library()


@register.filter(name='get_fieldname')
def get_fieldname(value, arg):
    """Register a template tag called getfieldname,
       which returns value from theme model"""
    theme = Theme.objects.all()

    for val in theme:
        if hasattr(val, str(arg)):
            return getattr(val, arg)

        else:
            return settings.str(arg)
