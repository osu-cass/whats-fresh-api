from django.http import (HttpResponse,
                         HttpResponseNotFound)
from django.contrib.gis.measure import D
from whats_fresh.whats_fresh_api.models import Vendor
from whats_fresh.whats_fresh_api.functions import get_lat_long_prox

import json
from .serializer import FreshSerializer


def vendor_list(request):
    """
    */vendors/*

    List all vendors in the database. There is no order to this list,
    only whatever is returned by the database.
    """
    error = {
        'status': False,
        'name': None,
        'text': None,
        'level': None,
        'debug': None
    }
    data = {}

    point, proximity, limit, error = get_lat_long_prox(request, error)

    if point:
        vendor_list = Vendor.objects.filter(
            location__distance_lte=(point, D(mi=proximity)))[:limit]
    else:
        vendor_list = Vendor.objects.all()[:limit]

    if not vendor_list:
        error = {
            "status": True,
            "name": "No Vendors",
            "text": "No Vendors found",
            "level": "Information",
            "debug": ""
        }

    serializer = FreshSerializer()

    data = {
        "vendors": json.loads(serializer.serialize(vendor_list)),
        "error": error
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


def vendors_products(request, id=None):
    """
    */vendors/products/<id>*

    List all vendors in the database that sell product <id>.
    There is no order to this list, only whatever is returned by the database.
    """
    error = {
        'status': False,
        'name': None,
        'text': None,
        'level': None,
        'debug': None
    }
    data = {}

    point, proximity, limit, error = get_lat_long_prox(request, error)
    try:
        if point:
            vendor_list = Vendor.objects.filter(
                vendorproduct__product_preparation__product__id__exact=id,
                location__distance_lte=(point, D(mi=proximity)))[:limit]
        else:
            vendor_list = Vendor.objects.filter(
                vendorproduct__product_preparation__product__id__exact=id
            )[:limit]

    except Exception as e:
        error = {
            'status': True,
            'name': 'Invalid product',
            'text': 'Product id is invalid',
            'level': 'Error',
            'debug': "{0}: {1}".format(type(e).__name__, str(e))
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    if not vendor_list:
        error = {
            "status": True,
            "name": "No Vendors",
            "text": "No Vendors found for product %s" % id,
            "level": "Information",
            "debug": ""
        }

    serializer = FreshSerializer()

    data = {
        "vendors": json.loads(serializer.serialize(vendor_list)),
        "error": error
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


def vendor_details(request, id=None):
    """
    */vendors/<id>*

    Returns the vendor data for vendor <id>.
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
        vendor = Vendor.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'status': True,
            'name': 'Vendor Not Found',
            'text': 'Vendor id %s was not found.' % id,
            'level': 'Error',
            'debug': "{0}: {1}".format(type(e).__name__, str(e))
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    serializer = FreshSerializer()

    data = json.loads(serializer.serialize(vendor))
    data['error'] = error

    return HttpResponse(json.dumps(data), content_type="application/json")
