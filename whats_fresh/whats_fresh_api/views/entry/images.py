from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from whats_fresh.whats_fresh_api.models import Image
from whats_fresh.whats_fresh_api.forms import ImageForm
from whats_fresh.whats_fresh_api.functions import group_required
from whats_fresh.whats_fresh_api.views.serializer import FreshSerializer
from whats_fresh.whats_fresh_api.templatetags import get_fieldname
from haystack.query import SearchQuerySet
from collections import OrderedDict


@login_required
@group_required('Administration Users', 'Data Entry Users')
def image_list(request):
    """
    */entry/images*

    The entry interface's images list. This view lists all images,
    their description, and allows you to click on them to view/edit the
    image.
    """

    message = ""
    if request.GET.get('success') == 'true':
        message = "Entry deleted successfully!"
    elif request.GET.get('saved') == 'true':
        message = "Entry saved successfully!"

    search = request.GET.get('search')

    if search is None or search.strip() == "":
        images = Image.objects.order_by('name')
    else:
        if request.GET.get('search') != "":
            images = list(
                OrderedDict.fromkeys(
                    item.object for item in
                    SearchQuerySet().models(Image).autocomplete(
                        content_auto=search)))
            if not images:
                message = "No results"

    paginator = Paginator(images, settings.PAGE_LENGTH)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        images = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        images = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {
        'message': message,
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'new_url': reverse('new-image'),
        'title': get_fieldname.get_fieldname('images'),
        'item_list': images,
        'edit_url': 'edit-image',
        'search_text': request.GET.get('search'),
        'list_url': get_fieldname.get_fieldname('images_slug')

    })


@login_required
@group_required('Administration Users', 'Data Entry Users')
def image(request, id=None):
    """
    */entry/images/<id>*, */entry/images/new*

    The entry interface's edit/add/delete image view. This view creates
    the edit page for a given image, or the "new image" page if it
    is not passed an ID. It also accepts POST requests to create or edit
    images.

    If called with DELETE, it will return a 200 upon success or a 404 upon
    failure. This is to be used as part of an AJAX call, or some other API
    call.
    """
    if request.method == 'DELETE':
        image = get_object_or_404(Image, pk=id)
        image.delete()
        return HttpResponse()

    if request.method == 'POST':
        message = ''

        if id:
            instance = get_object_or_404(Image, pk=id)
        else:
            instance = None
        image_form = ImageForm(
            request.POST,
            request.FILES,
            instance=instance)
        if image_form.is_valid():
            image_form.save()
            return HttpResponseRedirect(
                "%s?saved=true" % reverse('entry-list-images'))
        else:
            pass
    else:
        message = ''

    if id:
        image = Image.objects.get(id=id)
        title = "Edit {0}".format(image.name)
        post_url = reverse('edit-image', kwargs={'id': id})
        image_form = ImageForm(instance=image)

        if request.GET.get('success') == 'true':
            message = "Image saved successfully!"

    elif request.method != 'POST':
        image_form = ImageForm()
        post_url = reverse('new-image')
        title = "New " + get_fieldname.get_fieldname('images')

    else:
        post_url = reverse('new-image')
        title = "New " + get_fieldname.get_fieldname('images')

    return render(request, 'image.html', {
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('entry-list-images'),
             'name': get_fieldname.get_fieldname('images')}
        ],
        'title': title,
        'message': message,
        'post_url': post_url,
        'errors': [],
        'image_form': image_form,
    })


@login_required
@group_required('Administration Users', 'Data Entry Users')
def image_ajax(request, id=None):
    if request.method == 'GET':
        image_form = ImageForm()
        return render(request, 'image_ajax.html', {'image_form': image_form})

    elif request.method == 'POST':
        message = ''
        instance = None
        image_form = ImageForm(
            request.POST,
            request.FILES,
            instance=instance)
        if image_form.is_valid():
            image = image_form.save()
            serializer = FreshSerializer()
            return HttpResponse(serializer.serialize(image),
                                content_type="application/json")
        else:
            pass

        return render(request, 'image_ajax.html', {
            'message': message,
            'errors': [],
            'image_form': image_form})
