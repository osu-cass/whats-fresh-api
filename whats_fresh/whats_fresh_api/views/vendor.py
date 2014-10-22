from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from django.contrib.gis.measure import D
from django.contrib.gis.geos import fromstr
from whats_fresh.whats_fresh_api.models import Vendor, Product, VendorProduct
from django.forms.models import model_to_dict
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test

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

    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    proximity = request.GET.get('proximity', None)
    limit = request.GET.get('limit', None)

    if limit:
        try:
            limit = int(limit)
        except Exception as e:
            error = {
                'debug': "{0}: {1}".format(type(e).__name__, str(e)),
                'status': True,
                'level': 'Warning',
                'text': 'Invalid limit. Returning all results.',
                'name': 'Bad Limit'
            }
            limit = None

    if lat or lng:
        if proximity:
            try:
                proximity = int(proximity)
            except Exception as e:
                error = {
                    "level": "Warning",
                    "status": True,
                    "name": "Bad proximity",
                    "text": "There was an error finding vendors " \
                        "within {0} miles".format(proximity),
                    'debug': "{0}: {1}".format(type(e).__name__, str(e))
                }
                proximity = settings.DEFAULT_PROXIMITY
        else:
            proximity = settings.DEFAULT_PROXIMITY

        try:
            point = fromstr('POINT(%s %s)' % (lng, lat), srid=4326)
            vendor_list = Vendor.objects.filter(
                location__distance_lte=(point, D(mi=proximity)))[:limit]
        except Exception as e:
            error = {
                "level": "Warning",
                "status": True,
                "name": "Bad location",
                "text": "There was an error with the given "
                    "coordinates {0}, {1}".format(lat, lng),
                'debug': "{0}: {1}".format(type(e).__name__, str(e))
            }
            vendor_list = Vendor.objects.all()[:limit]
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

    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    proximity = request.GET.get('proximity', None)
    limit = request.GET.get('limit', None)

    if limit:
        try:
            limit = int(limit)
        except Exception as e:
            error = {
                'debug': "{0}: {1}".format(type(e).__name__, str(e)),
                'status': True,
                'level': 'Warning',
                'text': 'Invalid limit. Returning all results.',
                'name': 'Bad Limit'
            }
            limit = None

    if lat or lng:
        if proximity:
            try:
                proximity = int(proximity)
            except Exception as e:
                error = {
                    "level": "Warning",
                    "status": True,
                    "name": "Bad proximity",
                    "text": "There was an error finding vendors " \
                        "within {0} miles".format(proximity),
                    'debug': "{0}: {1}".format(type(e).__name__, str(e))
                }
                proximity = settings.DEFAULT_PROXIMITY
        else:
            proximity = settings.DEFAULT_PROXIMITY
        try:
            point = fromstr('POINT(%s %s)' % (lng, lat), srid=4326)
            vendor_list = Vendor.objects.filter(
                vendorproduct__product_preparation__product__id__exact=id,
                location__distance_lte=(point, D(mi=proximity)))[:limit]
        except Exception as e:
            error = {
                "level": "Warning",
                "status": True,
                "name": "Bad location",
                "text": "There was an error with the "
                    "given coordinates {0}, {1}".format(lat, lng),
                'debug': "{0}: {1}".format(type(e).__name__, str(e))
            }
            vendor_list = Vendor.objects.filter(
                vendorproduct__product_preparation__product__id__exact=id)[:limit]
    else:
        try:
            vendor_list = Vendor.objects.filter(
                vendorproduct__product_preparation__product__id__exact=id)[:limit]
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
            "level": "Error"
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
            )[1:-1] # Serializer can only serialize lists,
                    # so we have to chop off the list brackets
                    # to get the serialized string without the list
        )

    data['error'] = error

    return HttpResponse(json.dumps(data), content_type="application/json")

