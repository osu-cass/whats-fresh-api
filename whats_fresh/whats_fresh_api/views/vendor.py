from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from django.contrib.gis.measure import D
from django.contrib.gis.geos import fromstr
from whats_fresh_api.models import Vendor, Product, VendorProduct
from django.forms.models import model_to_dict
import json
from django.conf import settings


def vendor_list(request):
    data = {}

    lat = request.GET.get('lat', None)
    lng = request.GET.get('long', None)
    proximity = request.GET.get('proximity', None)

    if lat or lng:
        try:
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
            point = fromstr('POINT(%s %s)' % (lng, lat), srid=4326)
            vendor_list = Vendor.objects.filter(
                location__distance_lte=(point, D(mi=proximity)))
        except Exception as e:
            data['error'] = {
                "level": "Warning",
                "status": True,
                "name": "Bad location",
                "text": "There was an error with the given "
                    "coordinates {0}, {1}".format(lat, lng),
                'debug': "{0}: {1}".format(type(e).__name__, str(e))
            }
            vendor_list = Vendor.objects.all()
    else:
        vendor_list = Vendor.objects.all()

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
            data['vendors'][-1]['updated'] = str(vendor.modified)
            data['vendors'][-1]['ext'] = {}

            data['vendors'][-1]['id'] = vendor.id
            try:
                data['vendors'][-1]['story_id'] = vendor.story_id.id
            except:
                data['vendors'][-1]['story_id'] = None
            data['vendors'][-1]['lat'] = vendor.location.y
            data['vendors'][-1]['long'] = vendor.location.x

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
    data = {}

    lat = request.GET.get('lat', None)
    lng = request.GET.get('long', None)
    proximity = request.GET.get('proximity', None)

    if lat or lng:
        try:
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
            point = fromstr('POINT(%s %s)' % (lng, lat), srid=4326)
            vendor_list = Vendor.objects.filter(
                vendorproduct__product_preparation__product__id__exact=id,
                location__distance_lte=(point, D(mi=proximity)))
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
                vendorproduct__product_preparation__product__id__exact=id)
    else:
        try:
            vendor_list = Vendor.objects.filter(
                vendorproduct__product_preparation__product__id__exact=id)
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
            data['vendors'][-1]['updated'] = str(vendor.modified)
            data['vendors'][-1]['ext'] = {}
            data['vendors'][-1]['id'] = vendor.id

            data['vendors'][-1]['story_id'] = vendor.story_id.id

            data['vendors'][-1]['lat'] = vendor.location.y
            data['vendors'][-1]['long'] = vendor.location.x

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
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )


def vendor_details(request, id=None):
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

        data['story_id'] = vendor.story_id.id
        try:
            data['phone'] = vendor.phone.national_number
        except AttributeError:
            data['phone'] = None

        data['lat'] = vendor.location.y
        data['long'] = vendor.location.x

        data['created'] = str(vendor.created)
        data['updated'] = str(vendor.modified)
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
