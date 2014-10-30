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
        'level': None,
        'debug': None,
        'text': None,
        'name': None
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
            "text": "No Vendors found",
            "name": "No Vendors",
            "debug": "",
            "level": "Information"
        }

    serializer = FreshSerializer()

    data = {
        "vendors": json.loads(
            serializer.serialize(
                vendor_list,
                use_natural_foreign_keys=True
            )
        ),
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
        'level': None,
        'debug': None,
        'text': None,
        'name': None
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
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Error',
            'text': 'Product id is invalid',
            'name': 'Invalid product'
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    if not vendor_list:
        error = {
            "status": True,
            "text": "No Vendors found for product {}".format(id),
            "name": "No Vendors",
            "debug": "",
            "level": "Information"
        }

    serializer = FreshSerializer()

    data = {
        "vendors": json.loads(
            serializer.serialize(
                vendor_list,
                use_natural_foreign_keys=True
            )
        ),
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
        'level': None,
        'debug': None,
        'text': None,
        'name': None
    }

    try:
        vendor = Vendor.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'status': True,
            'level': 'Error',
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'text': 'Vendor id %s was not found.' % id,
            'name': 'Vendor Not Found'
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    serializer = FreshSerializer()

    data = json.loads(
        serializer.serialize(
            [vendor],
            use_natural_foreign_keys=True
        )[1:-1]  # Serializer can only serialize lists,
        # so we have to chop off the list brackets
        # to get the serialized string without the list
    )

    data['error'] = error

    return HttpResponse(json.dumps(data), content_type="application/json")
