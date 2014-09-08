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


def preparation_list(request):
    preparations = Preparation.objects.all()
    preparations_list = []

    for preparation in preparations:
        preparation_data = {}
        preparation_data['name'] = preparation.name
        preparation_data['description'] = preparation.description
        preparation_data['link'] = reverse('edit-preparation', kwargs={'id': preparation.id})

        if len(preparation_data['description']) > 100:
            preparation_data['description'] = preparation_data['description'][:100] + "..."

        preparations_list.append(preparation_data)

    return render(request, 'list.html', {
        'new_url': reverse('new-preparation'),
        'new_text': "New preparation",
        'title': "All preparations",
        'item_classification': "preparation",
        'item_list': preparations_list,
    })


def preparation(request, id=None):
    if request.method == 'POST':
        post_data = request.POST.copy()
        errors = []

        preparation_form = PreparationForm(post_data)
        if preparation_form.is_valid() and not errors:
            if id:
                preparation = Preparation.objects.get(id=id)
                preparation.__dict__.update(**preparation_form.cleaned_data)
                preparation.save()
            else:
                preparation = Preparation.objects.create(**preparation_form.cleaned_data)
                preparation.save()
            return HttpResponseRedirect("%s?success=true" % reverse('edit-preparation', kwargs={'id': preparation.id}))
        else:
            pass
    else:
        errors = []

    message = "Fields marked with bold are required."

    if id:
        preparation = Preparation.objects.get(id=id)
        title = "Edit {0}".format(preparation.name)
        post_url = reverse('edit-preparation', kwargs={'id': id})
        preparation_form = PreparationForm(instance=preparation)

        if request.GET.get('success') == 'true':
            message = "Preparation saved successfully!"

    elif request.method != 'POST':
        preparation_form = PreparationForm()
        post_url = reverse('new-preparation')
        title = "New Preparation"

    else:
        post_url = reverse('new-preparation')
        title = "New Preparation"

    return render(request, 'preparation.html', {
        'parent_url': reverse('entry-list-preparations'),
        'parent_text': 'Preparation List',
        'message': message,
        'title': title,
        'post_url': post_url,
        'errors': errors,
        'preparation_form': preparation_form,
    })
