from django.http import HttpResponse
from whats_fresh.whats_fresh_api.models import Vendor
import json


def locations(request):
    """
    */locations/*

    Returns a list of city names for all vendors. Useful for populating
    selection lists.
    """
    vendor_list = Vendor.objects.all()
    cities = [vendor.city for vendor in vendor_list]
    unique_cities = list(set(cities))
    data = {
        'locations': unique_cities,
        'error': {
            'status': False,
            'level': None,
            'text': None,
            'debug': None,
            'name': None
        }
    }
    return HttpResponse(json.dumps(data), content_type="application/json")