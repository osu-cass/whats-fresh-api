from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from whats_fresh.whats_fresh_api.models import Preparation
from django.forms.models import model_to_dict
import json


def preparation_details(request, id=None):
    """
    */preparations/<id>*

    Returns the preparation data for preparation <id>.
    """
    data = {}

    try:
        preparation = Preparation.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'status': True,
            'debug': '',
            'level': 'Important',
            'text': 'Preparation with id %s not found!' % id,
            'name': 'Preparation Not Found'
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    try:
        data = model_to_dict(preparation, fields=[], exclude=[])
        data['error'] = {
            'status': False,
            'level': None,
            'debug': None,
            'text': None,
            'name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        data['error'] = {
            'status': True,
            'level': 'Severe',
            'text': 'An unknown error occurred processing preparation %s' % id,
            'name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )
