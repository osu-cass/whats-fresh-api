from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from whats_fresh_api.models import Story
from django.forms.models import model_to_dict
import json


def story_details(request, id=None):
    data = {}

    try:
        story = Story.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'error_status': True,
            'error_level': 'Important',
            'error_text': 'Story with id %s not found!' % id,
            'error_name': 'Story Not Found'
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )
        
    try:
        data = model_to_dict(story, fields=[], exclude=[])
        del data['id']
        data['error'] = {
            'error_status': False,
            'error_level': None,
            'error_text': None,
            'error_name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except:
        data['error'] = {
            'error_status': True,
            'error_level': 'Severe',
            'error_text': 'An unknown error occurred processing story %s' % id,
            'error_name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )
