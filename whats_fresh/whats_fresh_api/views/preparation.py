from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from whats_fresh_api.models import Preparation
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
            'error_status': True,
            'error_level': 'Important',
            'error_text': 'Preparation with id %s not found!' % id,
            'error_name': 'Preparation Not Found'
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )
        
    try:
        data = model_to_dict(preparation, fields=[], exclude=[])
        data['error'] = {
            'error_status': False,
            'error_level': None,
            'error_text': None,
            'error_name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        data['error'] = {
            'error_status': True,
            'error_level': 'Severe',
            'error_text': 'An unknown error occurred processing preparation %s' % id,
            'error_name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )
