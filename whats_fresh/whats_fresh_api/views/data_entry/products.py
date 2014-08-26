from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError

from whats_fresh_api.models import *
from whats_fresh_api.forms import *
from whats_fresh_api.functions import *

import json


def product(request, id=None):
    if request.method == 'POST':
        post_data = request.POST.copy()
        errors = []

        try:
            if len(post_data['preparation_ids']) == 0:
                errors.append("You must choose at least one preparation.")
                preparations = []
            else:
                preparations = list(set(post_data['preparation_ids'].split(',')))
                post_data['preparations'] = 1 # Needed for form validation to pass
        except MultiValueDictKeyError:
            errors.append("You must choose at least one preparation.")
            preparations = []

        product_form = ProductForm(post_data)
        if product_form.is_valid() and not errors:
            del product_form.cleaned_data['preparations']
            product = Product.objects.create(**product_form.cleaned_data)
            for preparation in preparations:
                    product_preparation = ProductPreparation.objects.create(
                        product=product,
                        preparation=Preparation.objects.get(
                            id=preparation))
            product.save()
            return HttpResponseRedirect(reverse('products-list'))
        else:
            pass
    else:
        product_form = ProductForm()

    data = {'preparations': []}

    for preparation in Preparation.objects.all():
        data['preparations'].append({
            'id': preparation.id,
            'name': preparation.name
        })

    title = "New Product"
    post_url = reverse('new-product')

    message = "Fields marked with bold are required."

    json_preparations = json.dumps(data)

    return render(request, 'product.html', {
        'parent_url': reverse('products-list-edit'),
        'json_preparations': json_preparations,
        'preparation_dict': data,
        'parent_text': 'Product List',
        'message': message,
        'title': title,
        'post_url': post_url,
        'errors': [],
        'product_form': product_form,
    })

def product_list(request):
    pass
