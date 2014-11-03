from django.http import (HttpResponse,
                         HttpResponseNotFound)
from whats_fresh.whats_fresh_api.models import Product
from whats_fresh.whats_fresh_api.functions import get_limit

import json
from .serializer import FreshSerializer


def product_list(request):
    """
    */products/*

    Returns a list of all products in the database. The ?limit=<int> parameter
    limits the number of products returned.
    """
    error = {
        'status': False,
        'name': None,
        'text': None,
        'level': None,
        'debug': None
    }

    limit, error = get_limit(request, error)

    serializer = FreshSerializer()
    queryset = Product.objects.all()[:limit]

    if not queryset:
        error = {
            "status": True,
            "name": "No Products",
            "text": "No Products found",
            "level": "Information",
            "debug": ""
        }

    data = {
        "products": json.loads(
            serializer.serialize(
                queryset,
                use_natural_foreign_keys=True
            )
        ),
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
            'name': 'Product Not Found',
            'text': 'Product id %s was not found.' % id,
            'level': 'Error',
            'debug': '{0}: {1}'.format(type(e).__name__, str(e))
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    error = {
        'status': False,
        'name': None,
        'text': None,
        'level': None,
        'debug': None
    }

    serializer = FreshSerializer()

    data = json.loads(
        serializer.serialize(
            [product],
            use_natural_foreign_keys=True
        )[1:-1]
    )

    data['error'] = error

    return HttpResponse(json.dumps(data), content_type="application/json")


def product_vendor(request, id=None):
    """
    */products/vendors/<id>*

    List all products sold by vendor <id>. This information includes the
    details of the products, rather than only the product name/id and
    preparation name/id returned by */vendors/<id>*.
    """
    data = {}
    error = {
        'status': False,
        'name': None,
        'text': None,
        'level': None,
        'debug': None
    }
    limit, error = get_limit(request, error)

    try:
        product_list = Product.objects.filter(
            productpreparation__vendorproduct__vendor__id__exact=id)[:limit]
    except Exception as e:
        data['error'] = {
            'status': True,
            'name': 'Vendor Not Found',
            'text': 'Vendor with id %s not found!' % id,
            'level': 'Error',
            'debug': "{0}: {1}".format(type(e).__name__, str(e))
        }
        data['products'] = []
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    serializer = FreshSerializer()

    if not product_list:
        error = {
            "status": True,
            "name": "No Products",
            "text": "No Products found",
            "level": "Information",
            "debug": ""
        }

    data = {
        "products": json.loads(
            serializer.serialize(
                product_list,
                use_natural_foreign_keys=True
            )
        ),
        "error": error
    }

    return HttpResponse(json.dumps(data), content_type="application/json")
