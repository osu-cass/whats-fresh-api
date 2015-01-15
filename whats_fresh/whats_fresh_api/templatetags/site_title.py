from django import template
from django.conf import settings

register = template.Library()

@register.tag
def site_title(parser, token):
    """Register a template tag called site_title which returns SITE_TITLE"""
    node = template.Node()
    node.render = lambda: settings.SITE_TITLE
    return node
