from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from django.http import HttpResponseRedirect
from django.shortcuts import render

from whats_fresh_api.models import *
from whats_fresh_api.forms import *
from whats_fresh_api.functions import *

import json


def new_vendor(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        coordinates = get_coordinates_from_address(post_data['street'], post_data['city'], post_data['state'], post_data['zip'])
        post_data['lat'], post_data['long'] = float(coordinates[0]), float(coordinates[1])
        vendor_form = VendorForm(post_data)
        if vendor_form.is_valid():
            vendor_form.save()
            return HttpResponseRedirect(reverse('vendors-list'))
        print vendor_form.errors
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

