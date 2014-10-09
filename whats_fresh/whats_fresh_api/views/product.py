from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from whats_fresh.whats_fresh_api.models import Vendor, Product, VendorProduct
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, user_passes_test

import json
from .serializer_two import CleanSerializer


def product_list(request):
    """
    */products/*

    Returns a list of all products in the database. In the future this function
    will support the ?limit=<int> parameter to limit the number of products
    returned.
    """
    limit = request.GET.get('limit', None)
    if limit:
        limit = int(limit)

    error = {
        'status': False,
        'level': None,
        'debug': None,
        'text': None,
        'name': None
    }

    serializer = CleanSerializer()
    serializer.use_natural_keys()

    data = {
        "products": json.loads(
            serializer.serialize(Product.objects.all()[:limit])),
        "error": error
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


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
        del data['image']

        try:
            data['image'] = product.image.image.url
        except AttributeError:
            data['image'] = None
        try:
            data['story'] = product.story.id
        except AttributeError:
            data['story'] = None

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
            del data['products'][-1]['image']

            try:
                data['products'][-1]['story'] = product.story.id
            except AttributeError:
                data['products'][-1]['story'] = None
            try:
                data['products'][-1]['image'] = product.image.image.url
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
