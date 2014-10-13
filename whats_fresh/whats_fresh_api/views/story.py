from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from whats_fresh.whats_fresh_api.models import Story
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, user_passes_test

import json


def story_details(request, id=None):
    """
    */stories/<id>*

    Returns the story data for story <id>.
    """
    data = {}

    try:
        story = Story.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'status': True,
            'level': 'Error',
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'text': 'Story id %s was not found.' % id,
            'name': 'Story Not Found'
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    try:
        data = model_to_dict(story, fields=[], exclude=[])
        del data['id']
        data['error'] = {
            'status': False,
            'level': None,
            'debug': None,
            'text': None,
            'name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except:
        data['error'] = {
            'status': True,
            'level': 'Error',
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'text': 'An unknown error occurred processing story %s' % id,
            'name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )
