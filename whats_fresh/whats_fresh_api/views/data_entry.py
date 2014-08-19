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


def vendor(request, id=None):
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

        product_preparations = list(set(post_data['preparation_ids'].split(',')))
        post_data['products_preparations'] = 1 # Needed for form validation to pass

        vendor_form = VendorForm(post_data)
        if vendor_form.is_valid() and not errors:
            del vendor_form.cleaned_data['products_preparations']
            if id:
                vendor = Vendor.objects.get(id=id)

                # For all of the current vendor products,
                for vendor_product in vendor.vendorproduct_set.all():
                    # Delete any that aren't in the returned list
                    if vendor_product.product_preparation.id not in product_preparations:
                        vendor_product.delete()
                    # And ignore any that are in both the existing and the returned list
                    elif vendor_product.product_preparation.id in product_preparations:
                        product_preparations.remove(vendor_product.product_preparation.id)
                # Then, create all of the new ones
                for product_preparation in product_preparations:
                    vendor_product = VendorProduct.objects.create(
                        vendor=vendor,
                        product_preparation=ProductPreparation.objects.get(
                            id=product_preparation))
                vendor.__dict__.update(**vendor_form.cleaned_data)
                vendor.save()
            else:
                vendor = Vendor.objects.create(**vendor_form.cleaned_data)
                for product_preparation in product_preparations:
                    vendor_product = VendorProduct.objects.create(
                        vendor=vendor,
                        product_preparation=ProductPreparation.objects.get(
                            id=product_preparation))
                vendor.save()
            print vendor.description
            return HttpResponseRedirect("%s?success=true" % reverse('edit-vendor', kwargs={'id': vendor.id}))

        existing_product_preparations = []
        for preparation_id in product_preparations:
            product_preparation_object = ProductPreparation.objects.get(id=preparation_id)
            existing_product_preparations.append({
                'id': preparation_id,
                'preparation_text': product_preparation_object.preparation.name,
                'product': product_preparation_object.product.name
            })
    else:
        existing_product_preparations = []
        errors = []

    message = "Fields marked in bold are required."

    if id:
        vendor = Vendor.objects.get(id=id)
        vendor_form = VendorForm(instance=vendor)
        title = "Edit %s" % vendor.name
        post_url = reverse('edit-vendor', kwargs={'id': id})
        # If the list already has items, we're coming back to it from above
        # And have already filled the list with the product preparations POSTed
        if not existing_product_preparations:
            for vendor_product in vendor.vendorproduct_set.all():
                existing_product_preparations.append({
                    'id': vendor_product.product_preparation.preparation.id,
                    'preparation_text': vendor_product.product_preparation.preparation.name,
                    'product': vendor_product.product_preparation.product.name
                })
        if request.GET.get('success') == 'true':
            message = "Vendor saved successfully!"
    else:
        title = "New Vendor"
        post_url = reverse('new-vendor')
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

    return render(request, 'vendor.html', {
        'message': message,
        'title': title,
        'post_url': post_url,
        'existing_product_preparations': existing_product_preparations,
        'errors': errors,
        'vendor_form': vendor_form,
        'json_preparations': json_preparations,
        'product_list': product_list,
    })
