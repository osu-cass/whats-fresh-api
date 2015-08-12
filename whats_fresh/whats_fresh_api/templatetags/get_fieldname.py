from django import template
from django.conf import settings
from whats_fresh.whats_fresh_api.models import Theme


register = template.Library()


@register.filter(name='get_fieldname')
def get_fieldname(arg):
    """Register a template tag called getfieldname,
       which returns value from theme model(if present) else
       returns the default theme value from settings"""
    try:
        theme = Theme.objects.get(active="Yes")
        if hasattr(theme, str(arg)):
            if arg == 'logo':
                if theme.logo is None or theme.logo == "":
                    return False
                else:
                    return settings.MEDIA_URL + str(getattr(theme, arg))
            else:
                return getattr(theme, arg)

    except Theme.DoesNotExist:
        if hasattr(settings, str(arg).upper()):
            return getattr(settings, arg.upper())
