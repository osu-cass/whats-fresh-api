from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from django.http import HttpResponseRedirect
from django.shortcuts import render

from whats_fresh_api.models import *
from whats_fresh_api.forms import *

import json


def new_vendor(request):
    if request.method == 'POST':
        print "posted!"
    else:
        vendor_form = VendorForm()

    data = {}
    product_list = []

    for product in Product.objects.all():
        product_list.append(product.name)
        data[str(product.name)] = []
        for preparation in product.productpreparation_set.all():
            data[str(product.name)].append({
                "value": preparation.id,
                "name": preparation.preparation.name
            })
    
    json_preparations = json.dumps(data)

    return render(request, 'new_vendor.html', {
        'vendor_form': vendor_form,
        'json_preparations': json_preparations,
        'product_list': product_list,
    })

