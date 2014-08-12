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
        for vendor in vendor_list:
            data[str(vendor.id)] = model_to_dict(vendor, fields=[], exclude=[])
            data[str(vendor.id)]['phone'] = data[
                str(vendor.id)]['phone'].national_number

            data[str(vendor.id)]['created'] = str(vendor.created)
            data[str(vendor.id)]['updated'] = str(vendor.modified)
            data[str(vendor.id)]['ext'] = {}
            del data[str(vendor.id)]['id']

            data[str(vendor.id)]['story'] = data[str(vendor.id)].pop('story_id')

            products = data[str(vendor.id)]['products']
            data[str(vendor.id)]['products'] = {}
            for product_id in products:
                product = VendorProduct.objects.get(id=product_id)
                product_data = {
                    'preparation': product.preparation.name,
                    'name': product.product.name
                }
                data[str(vendor.id)]['products'][product_id] = product_data

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
            'error_text': 'An unknown error occurred processing the vendors',
            'error_name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )


def vendors_products(request, id=None):
    data = {}
    try:
        vendor_list = Vendor.objects.filter(products__id__contains=id)
    except Exception as e:
        data['error'] = {
            'error_status': True,
            'error_level': 'Severe',
            'error_text': 'Product id is invalid',
            'error_name': 'Invalid product'
        }

    if len(vendor_list) == 0:
        data['error'] = {
            'error_status': True,
            'error_level': 'Important',
            'error_text': 'Could not find any vendors for product %s!' % id,
            'error_name': 'No Vendors for product %s' % id
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    try:
        for vendor in vendor_list:
            data[str(vendor.id)] = model_to_dict(vendor, fields=[], exclude=[])
            data[str(vendor.id)]['phone'] = data[
                str(vendor.id)]['phone'].national_number

            data[str(vendor.id)]['created'] = str(vendor.created)
            data[str(vendor.id)]['updated'] = str(vendor.modified)
            data[str(vendor.id)]['ext'] = {}
            del data[str(vendor.id)]['id']

            data[str(vendor.id)]['story'] = data[str(vendor.id)].pop('story_id')

            products = data[str(vendor.id)]['products']
            data[str(vendor.id)]['products'] = {}
            for product_id in products:
                product = VendorProduct.objects.get(id=product_id)
                product_data = {
                    'preparation': product.preparation.name,
                    'name': product.product.name
                }
                data[str(vendor.id)]['products'][product_id] = product_data

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
            'error_text': 'An unknown error occurred processing the vendors for product %s' % id,
            'error_name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )
