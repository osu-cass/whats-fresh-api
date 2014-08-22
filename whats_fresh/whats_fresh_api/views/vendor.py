from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from whats_fresh_api.models import Vendor, Product, VendorProduct
from django.forms.models import model_to_dict
import json


def vendor_list(request):
    data = {}
    vendor_list = Vendor.objects.all()

    if len(vendor_list) == 0:
        data['error'] = {
            'debug': '',
            'status': True,
            'level': 'Error',
            'text': 'No Vendors found',
            'name': 'No Vendors'
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )
    try:
        data['vendors'] = []
        for vendor in vendor_list:
            data['vendors'].append(model_to_dict(vendor, fields=[], exclude=[]))
            data['vendors'][-1]['phone'] = data['vendors'][-1]['phone'].national_number

            try:
                data['vendors'][-1]['phone'] = data['vendors'][-1]['phone'].national_number
            except AttributeError:
                data['vendors'][-1]['phone'] = None

            data['vendors'][-1]['created'] = str(vendor.created)
            data['vendors'][-1]['updated'] = str(vendor.modified)
            data['vendors'][-1]['ext'] = {}
            data['vendors'][-1]['story'] = data['vendors'][-1].pop('story_id')
            data['vendors'][-1]['id'] = vendor.id

            data['vendors'][-1]['lat'] = vendor.location.y
            data['vendors'][-1]['long'] = vendor.location.x

            del data['vendors'][-1]['products_preparations']

            vendor_products = vendor.vendorproduct_set.all()
            data['vendors'][-1]['products'] = []
            for vendor_product in vendor_products:
                product_data = {
                    'product_id': vendor_product.product_preparation.product.id,
                    'preparation_id': vendor_product.product_preparation.preparation.id,
                    'preparation': vendor_product.product_preparation.preparation.name,
                    'name': vendor_product.product_preparation.product.name
                }
                data['vendors'][-1]['products'].append(product_data)

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
            'text': e,
            'name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )


def vendors_products(request, id=None):
    data = {}
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
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Important',
            'text': 'Could not find any vendors for product %s!' % id,
            'name': 'No Vendors for product %s' % id
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    try:
        data['vendors'] = []
        for vendor in vendor_list:
            data['vendors'].append(model_to_dict(vendor, fields=[], exclude=[]))

            try:
                data['vendors'][-1]['phone'] = data['vendors'][-1]['phone'].national_number
            except AttributeError:
                data['vendors'][-1]['phone'] = None

            data['vendors'][-1]['created'] = str(vendor.created)
            data['vendors'][-1]['updated'] = str(vendor.modified)
            data['vendors'][-1]['ext'] = {}
            data['vendors'][-1]['id'] = vendor.id

            data['vendors'][-1]['story'] = data['vendors'][-1].pop('story_id')
            data['vendors'][-1]['lat'] = vendor.location.y
            data['vendors'][-1]['long'] = vendor.location.x

            del data['vendors'][-1]['products_preparations']

            vendor_products = vendor.vendorproduct_set.all()
            data['vendors'][-1]['products'] = []
            for vendor_product in vendor_products:
                product_data = {
                    'product_id': vendor_product.product_preparation.product.id,
                    'preparation_id': vendor_product.product_preparation.preparation.id,
                    'preparation': vendor_product.product_preparation.preparation.name,
                    'name': vendor_product.product_preparation.product.name
                }
                data['vendors'][-1]['products'].append(product_data)

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
            'text': 'Error {0} occurred processing the vendors for product {1}'.format(e, id),
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
        data = model_to_dict(vendor, fields=[], exclude=[])
<<<<<<< HEAD
=======

        data['story_id'] = vendor.story_id.id
        try:
            data['phone'] = vendor.phone.national_number
       except AttributeError:
            data['phone'] = None
>>>>>>> Write location-based tests

<<<<<<< HEAD
        data['story_id'] = vendor.story_id.id
        if data['phone']:
            data['phone'] = data['phone'].national_number
        else:
            data['phone'] = None
=======
        data['lat'] = vendor.location.y
        data['long'] = vendor.location.x
        del data['location']

>>>>>>> Update Vendor to use GeoDjango point rather than lat/long
        data['created'] = str(vendor.created)
        data['updated'] = str(vendor.modified)
        data['ext'] = {}
        data['story'] = data.pop('story_id')
        data['id'] = vendor.id

        del data['products_preparations']

        vendor_products = vendor.vendorproduct_set.all()
        data['products'] = []
        for vendor_product in vendor_products:
            product_data = {
                'product_id': vendor_product.product_preparation.product.id,
                'preparation_id': vendor_product.product_preparation.preparation.id,
                'preparation': vendor_product.product_preparation.preparation.name,
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
            'text': 'An unknown error occurred processing vendor %s'
            % id,
            'name': e
        }

        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )
