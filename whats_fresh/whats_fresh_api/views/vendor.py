from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from whats_fresh_api.models import Vendor, Product, VendorProduct
from django.forms.models import model_to_dict
import json


def vendor_list(request):
    """
    */vendors/*

    Returns a list of all vendors in the database. In the future this function
    will support the ?limit=<int> parameter to limit the number of vendors
    returned, the ?lat=<float>&long=<float> parameters to sort by location, and
    the ?proximity=<int> parameter to limit the distance of the vendors.
    """
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

            data[str(vendor.id)]['story'] = data[
                str(vendor.id)].pop('story_id')

            vendor_products = vendor.vendorproduct_set.all()
            data[str(vendor.id)]['products'] = {}
            for vendor_product in vendor_products:
                product_data = {
                    'preparation': vendor_product.preparation.name,
                    'name': vendor_product.product.name
                }
                data[str(vendor.id)]['products'][
                    vendor_product.product.id] = product_data

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
        vendor_list = Vendor.objects.filter(products__id__exact=id)
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
        return HttpResponse(
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

            data[str(vendor.id)]['story'] = data[
                str(vendor.id)].pop('story_id')

            vendor_products = vendor.vendorproduct_set.all()
            data[str(vendor.id)]['products'] = {}
            for vendor_product in vendor_products:
                product_data = {
                    'preparation': vendor_product.preparation.name,
                    'name': vendor_product.product.name
                }
                data[str(vendor.id)]['products'][
                    vendor_product.product.id] = product_data

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
        data['phone'] = data['phone'].national_number
        data['created'] = str(vendor.created)
        data['updated'] = str(vendor.modified)
        data['ext'] = {}

        vendor_products = vendor.vendorproduct_set.all()
        data['products'] = {}
        for vendor_product in vendor_products:
            product_data = {
                'preparation': vendor_product.preparation.name,
                'name': vendor_product.product.name
            }
            data['products'][
                vendor_product.product.id] = product_data

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

