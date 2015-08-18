from django.http import (HttpResponse,
                         HttpResponseNotFound)
from whats_fresh.whats_fresh_api.models import Theme

import json
from .serializer import FreshSerializer
from whats_fresh.whats_fresh_api.functions import get_limit


def theme_list(request):
    """
    */themes/*

    Returns a list of all themes in the database. The ?limit=<int> parameter
    limits the number of themes returned.
    """
    error = {
        'status': False,
        'name': None,
        'text': None,
        'level': None,
        'debug': None
    }

    limit, error = get_limit(request, error)

    serializer = FreshSerializer()
    queryset = Theme.objects.all()[:limit]

    if not queryset:
        error = {
            "status": True,
            "name": "No Themes",
            "text": "No Themes found",
            "level": "Information",
            "debug": ""
        }

    data = {
        "themes": json.loads(serializer.serialize(queryset)),
        "error": error
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


def theme_details(request, id=None):
    """
    */admin/whats_fresh_api/theme/<id>*

    Returns the theme data for theme <id>.
    """
    data = {}

    error = {
        'status': False,
        'name': None,
        'text': None,
        'level': None,
        'debug': None
    }

    try:
        theme = Theme.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'status': True,
            'name': 'Theme Not Found',
            'text': 'Theme id %s was not found.' % id,
            'level': 'Error',
            'debug': '{0}: {1}'.format(type(e).__name__, str(e))
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    serializer = FreshSerializer()

    data = json.loads(serializer.serialize(theme))
    print data

    data['error'] = error

    return HttpResponse(json.dumps(data), content_type="application/json")
