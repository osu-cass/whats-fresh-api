from django import template
from whats_fresh.whats_fresh_api.models import Theme


register = template.Library()


@register.tag
def getfieldname(value, arg):
    """Register a template tag called getfieldname,
       which returns value from theme model"""
    return {'theme': Theme.objects.all()}
