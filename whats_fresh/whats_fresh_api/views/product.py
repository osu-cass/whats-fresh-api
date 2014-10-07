from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from whats_fresh.whats_fresh_api.models import Vendor, Product, VendorProduct
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, user_passes_test

import json


def product_list(request):
    """
    */products/*

    Returns a list of all products in the database. In the future this function
    will support the ?limit=<int> parameter to limit the number of products
    returned.
    """
    data = {}
    limit = request.GET.get('limit', None)

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

    product_list = Product.objects.all()[:limit]

    if len(product_list) == 0:
        data['error'] = {
            'status': True,
            'level': 'Error',
            'debug': '',
            'text': 'No Products found',
            'name': 'No Products'
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    data['products'] = []
    try:
        for product in product_list:
            data['products'].append(
                model_to_dict(product, exclude=['preparations', 'image_id']))

            try:
                data['products'][-1]['image'] = product.image_id.image.url
            except AttributeError:
                data['products'][-1]['image'] = None
            try:
                data['products'][-1]['story_id'] = product.story_id.id
            except AttributeError:
                data['products'][-1]['story_id'] = None

            data['products'][-1]['created'] = str(product.created)
            data['products'][-1]['modified'] = str(product.modified)
            data['products'][-1]['id'] = product.id

        data['error'] = {
            'status': False,
            'level': None,
            'text': None,
            'debug': None,
            'name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        data['error'] = {
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Severe',
            'text': str(e),
            'name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )


def product_details(request, id=None):
    """
    */products/<id>*

    Returns the product data for product <id>.
    """
    data = {}

    try:
        product = Product.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'status': True,
            'level': 'Error',
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'text': 'Product id %s was not found.' % id,
            'name': 'Product Not Found'
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    try:
        data = model_to_dict(product, fields=[], exclude=[])
        del data['preparations']
        del data['image_id']

        try:
            data['image'] = product.image_id.image.url
        except AttributeError:
            data['image'] = None
        try:
            data['story_id'] = product.story_id.id
        except AttributeError:
            data['story_id'] = None

        data['created'] = str(product.created)
        data['updated'] = str(product.modified)
        data['id'] = product.id

        data['error'] = {
            'status': False,
            'level': None,
            'debug': None,
            'text': None,
            'name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except:
        text = 'An unknown error occurred processing product %s' % id
        data['error'] = {
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Severe',
            'text': text,
            'name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )


def product_vendor(request, id=None):
    """
    */products/vendors/<id>*

    List all products sold by vendor <id>. This information includes the details
    of the products, rather than only the product name/id and preparation name/id
    returned by */vendors/<id>*.
    """
    data = {}

    try:
        product_list = Product.objects.filter(
            productpreparation__vendorproduct__vendor__id__exact=id)
    except Exception as e:
        data['error'] = {
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Important',
            'text': 'Vendor with id %s not found!' % id,
            'name': 'Vendor Not Found'
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    data['products'] = []
    try:
        for product in product_list:
            data['products'].append(
                model_to_dict(product, fields=[], exclude=[]))
            del data['products'][-1]['preparations']
            del data['products'][-1]['image_id']

            try:
                data['products'][-1]['story_id'] = product.story_id.id
            except AttributeError:
                data['products'][-1]['story_id'] = None
            try:
                data['products'][-1]['image'] = product.image_id.image.url
            except AttributeError:
                data['products'][-1]['image'] = None
            data['products'][-1]['created'] = str(product.created)
            data['products'][-1]['modified'] = str(product.modified)
            data['products'][-1]['id'] = product.id

        data['error'] = {
            'status': False,
            'level': None,
            'debug': None,
            'text': None,
            'name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        text = 'An unknown error occurred processing product %s' % id
        data['error'] = {
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Severe',
            'text': text,
            'name': str(e)
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )
