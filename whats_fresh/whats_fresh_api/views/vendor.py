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
            'error_status': True,
            'error_level': 'Important',
            'error_text': 'Could not find any vendors!',
            'error_name': 'No Vendors'
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

            data['vendors'][-1]['created'] = str(vendor.created)
            data['vendors'][-1]['updated'] = str(vendor.modified)
            data['vendors'][-1]['ext'] = {}
            data['vendors'][-1]['story'] = data['vendors'][-1].pop('story_id')
            data['vendors'][-1]['id'] = vendor.id

            del data['vendors'][-1]['products_preparations']

            vendor_products = vendor.vendorproduct_set.all()
            data['vendors'][-1]['products'] = []
            for vendor_product in vendor_products:
                product_data = {
                    'id': vendor_product.product_preparation.product.id,
                    'preparation': vendor_product.product_preparation.preparation.name,
                    'name': vendor_product.product_preparation.product.name
                }
                data['vendors'][-1]['products'].append(product_data)

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
            'error_text': e,
            'error_name': 'Unknown'
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
            'error_status': True,
            'error_level': 'Severe',
            'error_text': 'Product id is invalid',
            'error_name': 'Invalid product'
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    if len(vendor_list) == 0:
        data['error'] = {
            'error_status': True,
            'error_level': 'Important',
            'error_text': 'Could not find any vendors for product %s!' % id,
            'error_name': 'No Vendors for product %s' % id
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    try:
        data['vendors'] = []
        for vendor in vendor_list:
            data['vendors'].append(model_to_dict(vendor, fields=[], exclude=[]))
            data['vendors'][-1]['phone'] = data['vendors'][-1]['phone'].national_number
            data['vendors'][-1]['created'] = str(vendor.created)
            data['vendors'][-1]['updated'] = str(vendor.modified)
            data['vendors'][-1]['ext'] = {}
            data['vendors'][-1]['id'] = vendor.id

            data['vendors'][-1]['story'] = data['vendors'][-1].pop('story_id')

            del data['vendors'][-1]['products_preparations']

            vendor_products = vendor.vendorproduct_set.all()
            data['vendors'][-1]['products'] = []
            for vendor_product in vendor_products:
                product_data = {
                    'id': vendor_product.product_preparation.product.id,
                    'preparation': vendor_product.product_preparation.preparation.name,
                    'name': vendor_product.product_preparation.product.name
                }
                data['vendors'][-1]['products'].append(product_data)

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
            'error_text': 'Error {0} occurred processing the vendors for product {1}'.format(e, id),
            'error_name': 'Unknown'
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
            'error_status': True,
            'error_level': 'Important',
            'error_text': 'Vendor with id %s not found!' % id,
            'error_name': 'Vendor not found'
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    try:
        data = model_to_dict(vendor, fields=[], exclude=[])

        data['story_id'] = vendor.story_id.id
        if data['phone']:
            data['phone'] = data['phone'].national_number
        else:
            data['phone'] = None
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
                'id': vendor_product.product_preparation.product.id,
                'preparation': vendor_product.product_preparation.preparation.name,
                'name': vendor_product.product_preparation.product.name
            }
            data['products'].append(product_data)

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
            'error_text': 'An unknown error occurred processing vendor %s'
            % id,
            'error_name': e
        }

        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )
