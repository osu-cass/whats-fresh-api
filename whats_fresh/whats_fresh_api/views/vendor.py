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

def vendor_list(request):
    """
    */vendors/*

    List all vendors in the database. There is no order to this list,
    only whatever is returned by the database.
    """

    data = {}

    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    proximity = request.GET.get('proximity', None)
    limit = request.GET.get('limit', None)

    if limit:
        try:
            limit = int(limit)
        except Exception as e:
            data['error'] = {
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
                data['error'] = {
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
            data['error'] = {
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

    if len(vendor_list) == 0:
        data['error'] = {
            'debug': '',
            'status': True,
            'level': 'Error',
            'text': 'No Vendors found',
            'name': 'No Vendors'
        }
        data['vendors'] = []
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )
    try:
        data['vendors'] = []
        for vendor in vendor_list:
            data['vendors'].append(
                model_to_dict(
                   vendor,
                   fields=[],
                   exclude=['location', 'phone', 'products_preparations']))

            try:
                data['vendors'][-1]['phone'] = vendor.phone.national_number
            except AttributeError:
                data['vendors'][-1]['phone'] = None

            data['vendors'][-1]['created'] = str(vendor.created)
            data['vendors'][-1]['modified'] = str(vendor.modified)
            data['vendors'][-1]['ext'] = {}

            data['vendors'][-1]['id'] = vendor.id
            try:
                data['vendors'][-1]['story'] = vendor.story.id
            except:
                data['vendors'][-1]['story'] = None
            data['vendors'][-1]['lat'] = vendor.location.y
            data['vendors'][-1]['lng'] = vendor.location.x

            vendor_products = vendor.vendorproduct_set.all()
            data['vendors'][-1]['products'] = []
            for vendor_product in vendor_products:
                product_data = {
                    'product_id':
                        vendor_product.product_preparation.product.id,
                    'preparation_id':
                        vendor_product.product_preparation.preparation.id,
                    'preparation':
                        vendor_product.product_preparation.preparation.name,
                    'name': vendor_product.product_preparation.product.name
                }
                data['vendors'][-1]['products'].append(product_data)

        if not 'error' in data:
            data['error'] = {
                'debug': None,
                'status': False,
                'level': None,
                'text': None,
                'name': None
            }
        return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data['error'] = {
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Error',
            'text': str(e),
            'name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )

def vendors_products(request, id=None):
    """
    */vendors/products/<id>*

    List all vendors in the database that sell product <id>.
    There is no order to this list, only whatever is returned by the database.
    """
    data = {}

    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    proximity = request.GET.get('proximity', None)
    limit = request.GET.get('limit', None)

    if limit:
        try:
            limit = int(limit)
        except Exception as e:
            data['error'] = {
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
                data['error'] = {
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
            data['error'] = {
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
            data['error'] = {
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

    if len(vendor_list) == 0:
        data['error'] = {
            'debug': '',
            'status': True,
            'level': 'Error',
            'text': 'No Vendors found for product {0}'.format(id),
            'name': 'No Vendors'
        }
        data['vendors'] = []
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    try:
        data['vendors'] = []
        for vendor in vendor_list:
            data['vendors'].append(
                model_to_dict(
                    vendor,
                    fields=[],
                    exclude=['location', 'phone', 'products_preparations']))

            try:
                data['vendors'][-1]['phone'] = vendor.phone.national_number
            except AttributeError:
                data['vendors'][-1]['phone'] = None

            data['vendors'][-1]['created'] = str(vendor.created)
            data['vendors'][-1]['modified'] = str(vendor.modified)
            data['vendors'][-1]['ext'] = {}
            data['vendors'][-1]['id'] = vendor.id

            try:
                data['vendors'][-1]['story'] = vendor.story.id
            except AttributeError:
                data['story'] = None

            data['vendors'][-1]['lat'] = vendor.location.y
            data['vendors'][-1]['lng'] = vendor.location.x

            vendor_products = vendor.vendorproduct_set.all()
            data['vendors'][-1]['products'] = []
            for vendor_product in vendor_products:
                product_data = {
                    'product_id':
                        vendor_product.product_preparation.product.id,
                    'preparation_id':
                        vendor_product.product_preparation.preparation.id,
                    'preparation':
                        vendor_product.product_preparation.preparation.name,
                    'name': vendor_product.product_preparation.product.name
                }
                data['vendors'][-1]['products'].append(product_data)

        if not 'error' in data:
            data['error'] = {
                'debug': None,
                'status': False,
                'level': None,
                'text': None,
                'name': None
            }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        data['error'] = {
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Error',
            'text': 'Error {0} occurred processing the '
                'vendors for product {1}'.format(e, id),
            'name': 'Unknown'
        }
        raise
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )

def vendor_details(request, id=None):
    """
    */vendors/<id>*

    Vendor details for vendor <id>.
    """
    data = {}

    try:
        vendor = Vendor.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Error',
            'text': 'Vendor id %s was not found.' % id,
            'name': 'Vendor Not Found'
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    try:
        data = model_to_dict(
            vendor, fields=[], exclude=[
                'location', 'phone', 'products_preparations'])

        try:
            data['story'] = vendor.story.id
        except AttributeError:
            data['story'] = None
        try:
            data['phone'] = vendor.phone.national_number
        except AttributeError:
            data['phone'] = None

        data['lat'] = vendor.location.y
        data['lng'] = vendor.location.x

        data['created'] = str(vendor.created)
        data['modified'] = str(vendor.modified)
        data['ext'] = {}
        data['id'] = vendor.id

        vendor_products = vendor.vendorproduct_set.all()
        data['products'] = []
        for vendor_product in vendor_products:
            product_data = {
                'product_id': vendor_product.product_preparation.product.id,
                'preparation_id':
                    vendor_product.product_preparation.preparation.id,
                'preparation':
                    vendor_product.product_preparation.preparation.name,
                'name': vendor_product.product_preparation.product.name
            }
            data['products'].append(product_data)

        data['error'] = {
            'debug': None,
            'status': False,
            'level': None,
            'text': None,
            'name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        data['error'] = {
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Error',
            'text': 'An unknown error occurred processing vendor %s' % id,
            'name': str(e)
        }

        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )
