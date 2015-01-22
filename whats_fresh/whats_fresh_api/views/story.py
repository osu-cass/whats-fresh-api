from django.http import (HttpResponse,
                         HttpResponseNotFound)
from whats_fresh.whats_fresh_api.models import Story

import json
from .serializer import FreshSerializer


def story_details(request, id=None):
    """
    */stories/<id>*

    Returns the story data for story <id>.
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
        story = Story.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'status': True,
            'name': 'Story Not Found',
            'text': 'Story id %s was not found.' % id,
            'level': 'Error',
            'debug': '{0}: {1}'.format(type(e).__name__, str(e))
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    serializer = FreshSerializer()

    data = json.loads(
        serializer.serialize(
            [story],
            use_natural_foreign_keys=True
        )[1:-1]  # Serializer can only serialize lists,
                 # so we have to chop off the list brackets
                 # to get the serialized string without the list
        )

    data['error'] = error

    return HttpResponse(json.dumps(data), content_type="application/json")

def stories_list(request):
    """
    */stories/*

    Returns a list of all stories in the database. The ?limit=<int> parameter
    limits the number of stories returned.
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
    queryset = Product.objects.all()[:limit]

    if not queryset:
        error = {
            "status": True,
            "name": "No Products",
            "text": "No Products found",
            "level": "Information",
            "debug": ""
        }
    data = {
        "products": json.loads(
            serializer.serialize(
                queryset,
                use_natural_foreign_keys=True
            )
        ),
        "error": error
    }
    return HttpResponse(json.dumps(data), content_type="application/json")
