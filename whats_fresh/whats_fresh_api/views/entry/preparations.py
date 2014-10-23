from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from whats_fresh.whats_fresh_api.models import Preparation
from whats_fresh.whats_fresh_api.forms import PreparationForm
from whats_fresh.whats_fresh_api.functions import group_required


@login_required
@group_required('Administration Users', 'Data Entry Users')
def prep_list(request):
    """
    */entry/preparations*

    The entry interface's preparations list. This view lists all preparations,
    their description, and allows you to click on them to view/edit the
    preparation.
    """
    preparations = Preparation.objects.all()
    preparations_list = []

    message = ""
    if request.GET.get('success') == 'true':
        message = "Preparation deleted successfully!"

    for preparation in preparations:
        preparation_data = {}
        preparation_data['name'] = preparation.name
        preparation_data['description'] = preparation.description
        preparation_data['link'] = reverse(
            'edit-preparation', kwargs={'id': preparation.id})

        if len(preparation_data['description']) > 100:
            preparation_data['description'] = preparation_data[
                'description'][:100] + "..."

        preparations_list.append(preparation_data)

    return render(request, 'list.html', {
        'message': message,
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'new_url': reverse('new-preparation'),
        'new_text': "New preparation",
        'title': "All preparations",
        'item_classification': "preparation",
        'item_list': preparations_list,
    })


@login_required
@group_required('Administration Users', 'Data Entry Users')
def preparation(request, id=None):
    """
    */entry/preparations/<id>*, */entry/preparations/new*

    The entry interface's edit/add/delete preparation view. This view creates
    the edit page for a given preparation, or the "new preparation" page if it
    is not passed an ID. It also accepts POST requests to create or edit
    preparations.

    If called with DELETE, it will return a 200 upon success or a 404 upon
    failure. This is to be used as part of an AJAX call, or some other API
    call.
    """
    if request.method == 'DELETE':
        preparation = get_object_or_404(Preparation, pk=id)
        preparation.delete()
        return HttpResponse()

    if request.method == 'POST':
        message = ''
        post_data = request.POST.copy()
        errors = []

        preparation_form = PreparationForm(post_data)
        if preparation_form.is_valid() and not errors:
            if id:
                preparation = Preparation.objects.get(id=id)
                preparation.__dict__.update(**preparation_form.cleaned_data)
                preparation.save()
            else:
                preparation = Preparation.objects.create(
                    **preparation_form.cleaned_data)
                preparation.save()
            return HttpResponseRedirect(
                "%s?success=true" % reverse(
                    'edit-preparation', kwargs={'id': preparation.id}))
        else:
            pass
    else:
        errors = []
        message = ''

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
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('entry-list-preparations'), 'name': 'Preparations'}
        ],
        'title': title,
        'message': message,
        'post_url': post_url,
        'errors': errors,
        'preparation_form': preparation_form,
    })
