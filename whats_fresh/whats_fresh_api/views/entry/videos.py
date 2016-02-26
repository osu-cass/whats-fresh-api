from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from whats_fresh.whats_fresh_api.models import Video
from whats_fresh.whats_fresh_api.forms import VideoForm
from whats_fresh.whats_fresh_api.functions import group_required
from whats_fresh.whats_fresh_api.views.serializer import FreshSerializer
from haystack.query import SearchQuerySet
from whats_fresh.whats_fresh_api.templatetags import get_fieldname
from collections import OrderedDict


@login_required
@group_required('Administration Users', 'Data Entry Users')
def video_list(request):
    """
    */entry/videos*

    The entry interface's videos list. This view lists all videos,
    their description, and allows you to click on them to view/edit the
    video.
    """

    message = ""
    if request.GET.get('success') == 'true':
        message = "Entry deleted successfully!"
    elif request.GET.get('saved') == 'true':
        message = "Entry saved successfully!"

    search = request.GET.get('search')

    if search is None or search.strip() == "":
        videos = Video.objects.order_by('name')
    else:
        if request.GET.get('search') != "":
            videos = list(
                OrderedDict.fromkeys(
                    item.object for item in
                    SearchQuerySet().models(Video).autocomplete(
                        content_auto=search)))
            if not videos:
                message = "No results"

    paginator = Paginator(videos, settings.PAGE_LENGTH)
    page = request.GET.get('page')

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        videos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        videos = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {
        'message': message,
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'new_url': reverse('new-video'),
        'title': get_fieldname.get_fieldname('videos'),
        'item_list': videos,
        'edit_url': 'edit-video',
        'search_text': request.GET.get('search'),
        'list_url': get_fieldname.get_fieldname('videos_slug')

    })


@login_required
@group_required('Administration Users', 'Data Entry Users')
def video(request, id=None):
    """
    */entry/videos/<id>*, */entry/videos/new*

    The entry interface's edit/add/delete video view. This view creates
    the edit page for a given video, or the "new video" page if it
    is not passed an ID. It also accepts POST requests to create or edit
    videos.

    If called with DELETE, it will return a 200 upon success or a 404 upon
    failure. This is to be used as part of an AJAX call, or some other API
    call.
    """
    if request.method == 'DELETE':
        video = get_object_or_404(Video, pk=id)
        video.delete()
        return HttpResponse()

    if request.method == 'POST':
        message = ''
        post_data = request.POST.copy()
        errors = []

        video_form = VideoForm(post_data)
        if video_form.is_valid() and not errors:
            if id:
                video = Video.objects.get(id=id)
                video.__dict__.update(**video_form.cleaned_data)
                video.save()
            else:
                video = Video.objects.create(
                    **video_form.cleaned_data)
                video.save()
            return HttpResponseRedirect(
                "%s?saved=true" % reverse('entry-list-videos'))
        else:
            pass
    else:
        errors = []
        message = ''

    if id:
        video = Video.objects.get(id=id)
        title = "Edit {0}".format(video.name)
        post_url = reverse('edit-video', kwargs={'id': id})
        video_form = VideoForm(instance=video)

        if request.GET.get('success') == 'true':
            message = "Video saved successfully!"

    elif request.method != 'POST':
        video_form = VideoForm()
        post_url = reverse('new-video')
        title = "New " + get_fieldname.get_fieldname('videos')

    else:
        post_url = reverse('new-video')
        title = "New " + get_fieldname.get_fieldname('videos')

    return render(request, 'video.html', {
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('entry-list-videos'),
             'name': get_fieldname.get_fieldname('videos')}
        ],
        'title': title,
        'message': message,
        'post_url': post_url,
        'errors': errors,
        'video_form': video_form,
    })


@login_required
@group_required('Administration Users', 'Data Entry Users')
def video_ajax(request, id=None):
    if request.method == 'GET':
        video_form = VideoForm()
        return render(request, 'video_ajax.html', {'video_form': video_form})

    elif request.method == 'POST':
        message = ''
        post_data = request.POST.copy()
        errors = []

        video_form = VideoForm(post_data)
        if video_form.is_valid() and not errors:
            video = Video.objects.create(
                **video_form.cleaned_data)
            video.save()
            serializer = FreshSerializer()
            return HttpResponse(serializer.serialize(video),
                                content_type="application/json")
        else:
            pass

        return render(request, 'video_ajax.html', {
            'message': message,
            'errors': errors,
            'video_form': video_form})
