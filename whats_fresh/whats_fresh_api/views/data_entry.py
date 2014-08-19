from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from whats_fresh_api.models import *
from whats_fresh_api.forms import *
from whats_fresh_api.functions import *

import json


def new_vendor(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        errors = []

        try:
            coordinates = get_coordinates_from_address(
                post_data['street'], post_data['city'], post_data['state'],
                post_data['zip'])
            post_data['lat'] = float(coordinates[0])
            post_data['long'] = float(coordinates[1])
        except BadAddressException:
            errors.append("Bad address!")

        if len(post_data['preparation_ids']) == 0:
            errors.append("You must choose at least one product.")

        product_preparations = post_data['preparation_ids'].split(',')
        post_data['products_preparations'] = 1 # Needed for form validation to pass

        vendor_form = VendorForm(post_data)
        if vendor_form.is_valid() and not errors:
            del vendor_form.cleaned_data['products_preparations']
            vendor = Vendor.objects.create(**vendor_form.cleaned_data)
            for product_preparation in product_preparations:
                vendor_product = VendorProduct.objects.create(
                    vendor=vendor,
                    product_preparation=ProductPreparation.objects.get(
                        id=product_preparation))
            return HttpResponseRedirect(reverse('edit-vendor', kwargs={'id': vendor.id}))
    else:
        errors = []
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
        'errors': errors,
        'vendor_form': vendor_form,
        'json_preparations': json_preparations,
        'product_list': product_list,
    })


def edit_vendor(request, id=None):
    vendor = Vendor.objects.get(id=id)
    vendor_form = VendorForm(instance=vendor)

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

    return render(request, 'edit_vendor.html', {
        'vendor_form': vendor_form,
        'json_preparations': json_preparations,
        'product_list': product_list,
    })
