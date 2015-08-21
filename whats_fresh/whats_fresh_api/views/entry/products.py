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
from whats_fresh.whats_fresh_api.views.serializer import FreshSerializer
from whats_fresh.whats_fresh_api.templatetags import get_fieldname

from haystack.query import SearchQuerySet
from collections import OrderedDict
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
                errors.append(
                    "You must choose at least one entry from "
                    + get_fieldname.get_fieldname('preparations'))
                preparations = []
            else:
                preparations = [int(p) for p in set(
                    post_data['preparation_ids'].split(','))]
        except MultiValueDictKeyError:
            errors.append(
                "You must choose at least one entry from "
                + get_fieldname.get_fieldname('preparations'))
            preparations = []

        if id:
            product = Product.objects.get(id=id)
        else:
            product = None

        product_form = ProductForm(post_data, product)
        if product_form.is_valid() and not errors:
            if id:
                for product_preparation in (
                        ProductPreparation.objects.filter(product=product)
                        .exclude(preparation__id__in=preparations)):
                    product_preparation.delete()

                existing_preparations = [
                    pp.preparation.id for pp in
                        ProductPreparation.objects.filter(
                            product=product,
                            preparation__id__in=preparations)
                ]

                for preparation in preparations:
                    if preparation not in existing_preparations:
                        ProductPreparation.objects.create(
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
        title = "New " + get_fieldname.get_fieldname('products')
        existing_preparations = []

    else:
        post_url = reverse('new-product')
        title = "New " + get_fieldname.get_fieldname('products')
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
            {'url': reverse('entry-list-products'),
             'name': get_fieldname.get_fieldname('products')}],
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
        message = "Entry deleted successfully!"
    elif request.GET.get('saved') == 'true':
        message = "Entry saved successfully!"

    search = request.GET.get('search')

    if search is None or search.strip() == "":
        products = Product.objects.order_by('name')
    else:
        if request.GET.get('search') != "":
            products = list(
                OrderedDict.fromkeys(
                    item.object for item in
                    SearchQuerySet().models(Product).autocomplete(
                        content_auto=search)))
            if not products:
                message = "No results"

    paginator = Paginator(products, settings.PAGE_LENGTH)

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
        'title': get_fieldname.get_fieldname('products'),
        'item_list': products,
        'description_field': {'title': 'Variety', 'attribute': 'variety'},
        'edit_url': 'edit-product',
        'search_text': request.GET.get('search'),
        'list_url': get_fieldname.get_fieldname('products_slug')

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

        return render(request, 'product_ajax.html',
                      {'product_form': product_form,
                       'json_preparations': json_preparations,
                       'preparation_dict': data})

    elif request.method == 'POST':
        message = ''
        post_data = request.POST.copy()
        errors = []

        try:
            if len(post_data['prep_ids']) == 0:
                errors.append(
                    "You must choose at least one entry from "
                    + get_fieldname.get_fieldname('preparations'))
                preparations = []
            else:
                preparations = [int(p) for p in set(
                    post_data['prep_ids'].split(','))]
        except MultiValueDictKeyError:
            errors.append("You must choose at least one entry from " +
                          get_fieldname.get_fieldname('preparations'))
            preparations = []

        product = None

        product_form = ProductForm(post_data, product)
        popup_prep = []
        if product_form.is_valid() and not errors:
            product = Product.objects.create(**product_form.cleaned_data)
            for preparation in preparations:
                inline_prep = ProductPreparation.objects.create(
                    product=product,
                    preparation=Preparation.objects.get(
                        id=preparation))
                popup_prep.append({
                    'id': inline_prep.id,
                    'name': inline_prep.preparation.name
                })
                product.save()
            serializer = FreshSerializer()
            data = json.loads(serializer.serialize(product))
            data['preparations'] = popup_prep
            return HttpResponse(json.dumps(data),
                                content_type="application/json")

        data = {'preparations': []}

        for preparation in Preparation.objects.all():
            data['preparations'].append({
                'id': preparation.id,
                'name': preparation.name})

        json_preparations = json.dumps(data)

        return render(request, 'product_ajax.html', {
            'json_preparations': json_preparations,
            'preparation_dict': data,
            'parent_text': 'Product List',
            'message': message,
            'errors': errors,
            'product_form': product_form})
