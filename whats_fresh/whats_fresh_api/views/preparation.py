from django.http import (HttpResponse,
                         HttpResponseNotFound)
from whats_fresh.whats_fresh_api.models import Preparation

import json
from .serializer import FreshSerializer


def preparation_details(request, id=None):
    """
    */preparations/<id>*

    Returns the preparation data for preparation <id>.
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
        preparation = Preparation.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'status': True,
            'name': 'Preparation Not Found',
            'text': 'Preparation id %s was not found.' % id,
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
            [preparation],
            use_natural_foreign_keys=True
        )[1:-1]  # Serializer can only serialize lists,
        # so we have to chop off the list brackets
        # to get the serialized string without the list
    )

    data['error'] = error

    return HttpResponse(json.dumps(data), content_type="application/json")
