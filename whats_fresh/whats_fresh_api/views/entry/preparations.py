from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from whats_fresh.whats_fresh_api.models import Preparation
from whats_fresh.whats_fresh_api.forms import PreparationForm
from whats_fresh.whats_fresh_api.functions import group_required
from whats_fresh.whats_fresh_api.views.serializer import FreshSerializer
from whats_fresh.whats_fresh_api.templatetags import get_fieldname
from haystack.query import SearchQuerySet
from collections import OrderedDict


@login_required
@group_required('Administration Users', 'Data Entry Users')
def prep_list(request):
    """
    */entry/preparations*

    The entry interface's preparations list. This view lists all preparations,
    their description, and allows you to click on them to view/edit the
    preparation.
    """

    message = ""
    if request.GET.get('success') == 'true':
        message = "Entry deleted successfully!"
    elif request.GET.get('saved') == 'true':
        message = "Entry saved successfully!"

    search = request.GET.get('search')

    if search is None or search.strip() == "":
        preparations = Preparation.objects.order_by('name')
    else:
        if request.GET.get('search') != "":
            preparations = list(
                OrderedDict.fromkeys(
                    item.object for item in
                    SearchQuerySet().models(Preparation).autocomplete(
                        content_auto=search)))
            if not preparations:
                message = "No results"

    paginator = Paginator(preparations, settings.PAGE_LENGTH)
    page = request.GET.get('page')

    try:
        preparations = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        preparations = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        preparations = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {
        'message': message,
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'new_url': reverse('new-preparation'),
        'title': get_fieldname.get_fieldname('preparations'),
        'item_list': preparations,
        'edit_url': 'edit-preparation',
        'search_text': request.GET.get('search'),
        'list_url': get_fieldname.get_fieldname('preparations_slug')

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
                "%s?saved=true" % reverse('entry-list-preparations'))
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
            message = "Item saved successfully!"

    elif request.method != 'POST':
        preparation_form = PreparationForm()
        post_url = reverse('new-preparation')
        title = "New " + get_fieldname.get_fieldname('preparations')

    else:
        post_url = reverse('new-preparation')
        title = "New " + get_fieldname.get_fieldname('preparations')

    return render(request, 'preparation.html', {
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('entry-list-preparations'),
             'name': get_fieldname.get_fieldname('preparations')}
        ],
        'title': title,
        'message': message,
        'post_url': post_url,
        'errors': errors,
        'preparation_form': preparation_form,
    })


@login_required
@group_required('Administration Users', 'Data Entry Users')
def preparation_ajax(request, id=None):
    if request.method == 'GET':
        preparation_form = PreparationForm()
        return render(request, 'preparation_ajax.html',
                      {'preparation_form': preparation_form})

    elif request.method == 'POST':
        message = ''
        post_data = request.POST.copy()
        errors = []

        preparation_form = PreparationForm(post_data)
        if preparation_form.is_valid() and not errors:
            preparation = Preparation.objects.create(
                **preparation_form.cleaned_data)
            preparation.save()
            serializer = FreshSerializer()
            return HttpResponse(serializer.serialize(preparation),
                                content_type="application/json")
        else:
            pass

        return render(request, 'preparation_ajax.html', {
            'message': message,
            'errors': errors,
            'preparation_form': preparation_form})
