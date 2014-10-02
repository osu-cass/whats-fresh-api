from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.gis.geos import fromstr

from whats_fresh.whats_fresh_api.models import *
from whats_fresh.whats_fresh_api.forms import *
from whats_fresh.whats_fresh_api.functions import *

import json


def vendor(request, id=None):
    """
    */entry/vendors/<id>*, */entry/vendors/new*

    The entry interface's edit/add vendor view. This view creates the edit
    page for a given vendor, or the "new vendor" page if it is not passed
    an ID. It also accepts POST requests to create or edit vendors.
    """
    if request.method == 'POST':
        post_data = request.POST.copy()
        errors = []

        try:
            coordinates = get_coordinates_from_address(
                post_data['street'], post_data['city'], post_data['state'],
                post_data['zip'])

            post_data['location'] = fromstr(
                'POINT(%s %s)' % (coordinates[1], coordinates[0]),
                srid=4326)
        # Bad Address will be thrown if Google does not return coordinates for
        # the address, and MultiValueDictKeyError will be thrown if the POST
        # data being passed in is empty.
        except BadAddressException:
            errors.append("Bad address!")
        except MultiValueDictKeyError:
            errors.append("Full address is required.")

        try:
            if len(post_data['preparation_ids']) == 0:
                errors.append("You must choose at least one product.")
                product_preparations = []
            else:
                product_preparations = list(set(post_data['preparation_ids'].split(',')))
                # TODO: Find better way to do form validation
                post_data['products_preparations'] = product_preparations[0] # Needed for form validation to pass
        except MultiValueDictKeyError:
            errors.append("You must choose at least one product.")
            product_preparations = []

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

    if id:
        vendor = Vendor.objects.get(id=id)
        vendor_form = VendorForm(instance=vendor)
        title = "Edit %s" % vendor.name
        message = "* = Required field"
        post_url = reverse('edit-vendor', kwargs={'id': id})
        # If the list already has items, we're coming back to it from above
        # And have already filled the list with the product preparations POSTed
        if not existing_product_preparations:
            for vendor_product in vendor.vendorproduct_set.all():
                existing_product_preparations.append({
                    'id': vendor_product.product_preparation.id,
                    'preparation_text': vendor_product.product_preparation.preparation.name,
                    'product': vendor_product.product_preparation.product.name
                })
        if request.GET.get('success') == 'true':
            message = "Vendor saved successfully!"
    elif request.method != 'POST':
        title = "Add a Vendor"
        post_url = reverse('new-vendor')
        message = "* = Required field"
        vendor_form = VendorForm()
    else:
        title = "Add aVendor"
        message = "* = Required field"
        post_url = reverse('new-vendor')

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
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('list-vendors-edit'), 'name': 'Vendors'}],
        'title': title,
        'message': message,
        'post_url': post_url,
        'existing_product_preparations': existing_product_preparations,
        'errors': errors,
        'vendor_form': vendor_form,
        'json_preparations': json_preparations,
        'product_list': product_list,
    })


def vendor_list(request):
    """
    */entry/vendors*

    The entry interface's vendors list. This view lists all vendors,
    their description, and allows you to click on them to view/edit the
    vendor.
    """
    vendors = Vendor.objects.all()
    vendors_list = []

    for vendor in vendors:
        vendor_data = {}
        vendor_data['name'] = vendor.name
        vendor_data['modified'] = vendor.modified.strftime("%I:%M %P, %d %b %Y")
        vendor_data['description'] = vendor.description
        vendor_data['link'] = reverse('edit-vendor', kwargs={'id': vendor.id})

        if len(vendor_data['description']) > 100:
            vendor_data['description'] = vendor_data['description'][:100] + "..."

        vendors_list.append(vendor_data)

    return render(request, 'list.html', {
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'new_url': reverse('new-vendor'),
        'new_text': "New Vendor",
        'title': "All Vendors",
        'item_classification': "vendor",
        'item_list': vendors_list,
    })
