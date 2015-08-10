from django import template
from django.conf import settings
from whats_fresh.whats_fresh_api.models import Theme


register = template.Library()


@register.filter(name='get_fieldname')
def get_fieldname(arg):
    """Register a template tag called getfieldname,
       which returns value from theme model(if present) else
       returns the default theme value from settings"""
    theme = Theme.objects.all()

    if theme:
        for val in theme:
            if hasattr(val, str(arg)):
                if arg == 'logo':
                    return settings.MEDIA_URL + str(getattr(val, arg))
                else:
                    return getattr(val, arg)

    else:
        if hasattr(settings, str(arg).upper()):
            return getattr(settings, arg.upper())
