from django.http import (HttpResponse, HttpResponseRedirect)
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.forms.models import save_instance

from whats_fresh.whats_fresh_api.models import (Product, Preparation,
                                                ProductPreparation)
from whats_fresh.whats_fresh_api.forms import ProductForm
from whats_fresh.whats_fresh_api.functions import group_required

import json


@login_required
@group_required('Administration Users', 'Data Entry Users')
def product(request, id=None):
    """
    */entry/products/<id>*, */entry/products/new*

    The entry interface's edit/add/delete product view. This view creates the
    edit page for a given product, or the "new product" page if it is not
    passed an ID. It also accepts POST requests to create or edit products, and
    DELETE requests to delete them.

    If called with DELETE, it will return a 200 upon success or a 404 upon
    failure. This is to be used as part of an AJAX call, or some other API
    call.
    """
    if request.method == 'DELETE':
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return HttpResponse()

    if request.method == 'POST':
        message = ''
        post_data = request.POST.copy()
        errors = []

        try:
            if len(post_data['preparation_ids']) == 0:
                errors.append("You must choose at least one preparation.")
                preparations = []
            else:
                preparations = [int(p) for p in set(
                    post_data['preparation_ids'].split(','))]
        except MultiValueDictKeyError:
            errors.append("You must choose at least one preparation.")
            preparations = []

        if id:
            product = Product.objects.get(id=id)
        else:
            product = None

        product_form = ProductForm(post_data, product)
        if product_form.is_valid() and not errors:
            if id:
                for preparation in product.preparations.all():
                    # Delete any that aren't in the returned list
                    if preparation.id not in preparations:
                        product_preparation = ProductPreparation.objects.get(
                            product=product, preparation=preparation)
                        product_preparation.delete()
                    # And ignore any that are in both the existing and the
                    # returned list
                    elif preparation.id in preparations:
                        preparations.remove(preparation.id)
                # Then, create all of the new ones
                for preparation in preparations:
                    preparation = ProductPreparation.objects.create(
                        product=product,
                        preparation=Preparation.objects.get(
                            id=preparation))
                save_instance(product_form, product)
            else:
                product = Product.objects.create(**product_form.cleaned_data)
                for preparation in preparations:
                    product_preparation = ProductPreparation.objects.create(
                        product=product,
                        preparation=Preparation.objects.get(
                            id=preparation))
                product.save()
            return HttpResponseRedirect(
                "%s?saved=true" % reverse('entry-list-products'))
    else:
        errors = []
        message = ''

    if id:
        product = Product.objects.get(id=id)
        title = "Edit {0}".format(product.name)
        post_url = reverse('edit-product', kwargs={'id': id})
        product_form = ProductForm(instance=product)

        existing_preparations = product.preparations.all()

        if request.GET.get('success') == 'true':
            message = "Product saved successfully!"

    elif request.method != 'POST':
        product_form = ProductForm()
        post_url = reverse('new-product')
        title = "New Product"
        existing_preparations = []

    else:
        post_url = reverse('new-product')
        title = "New Product"
        existing_preparations = []

    data = {'preparations': []}

    for preparation in Preparation.objects.all():
        data['preparations'].append({
            'id': preparation.id,
            'name': preparation.name
        })

    json_preparations = json.dumps(data)

    return render(request, 'product.html', {
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('entry-list-products'), 'name': 'Products'}],
        'json_preparations': json_preparations,
        'preparation_dict': data,
        'existing_preparations': existing_preparations,
        'parent_text': 'Product List',
        'message': message,
        'title': title,
        'post_url': post_url,
        'errors': errors,
        'product_form': product_form,
    })


@login_required
@group_required('Administration Users', 'Data Entry Users')
def product_list(request):
    """
    */entry/products*

    The entry interface's products list. This view lists all products,
    their description, and allows you to click on them to view/edit the
    product.
    """

    message = ""
    if request.GET.get('success') == 'true':
        message = "Product deleted successfully!"
    elif request.GET.get('saved') == 'true':
        message = "Product saved successfully!"

    paginator = Paginator(Product.objects.order_by('name'),
                          settings.PAGE_LENGTH)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {
        'message': message,
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'new_url': reverse('new-product'),
        'new_text': "New product",
        'title': "All Products",
        'item_classification': "product",
        'item_list': products,
        'description_field': {'title': 'Variety', 'attribute': 'variety'},
        'edit_url': 'edit-product'
    })


@login_required
@group_required('Administration Users', 'Data Entry Users')
def product_ajax(request, id=None):
    if request.method == 'GET':
        product_form = ProductForm()

        data = {'preparations': []}

        for preparation in Preparation.objects.all():
            data['preparations'].append({
                'id': preparation.id,
                'name': preparation.name
            })

        json_preparations = json.dumps(data)

        return render(request, 'product_ajax.html', {'product_form': product_form, 'json_preparations': json_preparations,
        'preparation_dict': data})

    elif request.method == 'POST':
        message = ''
        post_data = request.POST.copy()
        errors = []

        try:
            if len(post_data['preparation_ids']) == 0:
                errors.append("You must choose at least one preparation.")
                preparations = []
            else:
                preparations = [int(p) for p in set(
                    post_data['preparation_ids'].split(','))]
        except MultiValueDictKeyError:
            errors.append("You must choose at least one preparation.")
            preparations = []

        product = None

        product_form = ProductForm(post_data, product)
        if product_form.is_valid() and not errors:
            product = Product.objects.create(**product_form.cleaned_data)
            for preparation in preparations:
                product_preparation = ProductPreparation.objects.create(
                    product=product,
                    preparation=Preparation.objects.get(
                        id=preparation))
            product.save()
            # return HttpResponseRedirect(
            #     "%s?saved=true" % reverse('entry-list-products'))
    else:
        errors = []
        message = ''


    data = {'preparations': []}

    for preparation in Preparation.objects.all():
       data['preparations'].append({
           'id': preparation.id,
           'name': preparation.name
       })

    json_preparations = json.dumps(data)

    return render(request, 'product.html', {
       'parent_url': [
           {'url': reverse('home'), 'name': 'Home'},
           {'url': reverse('entry-list-products'), 'name': 'Products'}],
       'json_preparations': json_preparations,
       'preparation_dict': data,
       'existing_preparations': existing_preparations,
       'parent_text': 'Product List',
       'message': message,
       'errors': errors,
       'product_form': product_form,
   })
