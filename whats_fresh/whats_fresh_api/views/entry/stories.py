from django.http import HttpResponse, HttpResponseRedirect
from whats_fresh.whats_fresh_api.models import Story, Image, Video
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from whats_fresh.whats_fresh_api.functions import group_required
from django.conf import settings
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from whats_fresh.whats_fresh_api.forms import StoryForm
from whats_fresh.whats_fresh_api.templatetags import get_fieldname

import json


@login_required
@group_required('Administration Users', 'Data Entry Users')
def story_list(request):
    """
    */entry/stories*

    The entry interface's stories list. This view lists all stories,
    their description, and allows you to click on them to view/edit the
    story.
    """

    message = ""
    if request.GET.get('success') == 'true':
        message = "Story deleted successfully!"

    paginator = Paginator(Story.objects.order_by('name'), settings.PAGE_LENGTH)
    page = request.GET.get('page')

    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        stories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        stories = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {
        'message': message,
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'new_url': reverse('new-story'),
        'new_text': "New Item",
        'title': get_fieldname.get_fieldname('stories', 'stories'),
        'item_classification': "item",
        'item_list': stories,
        'edit_url': 'edit-story'
    })


@login_required
@group_required('Administration Users', 'Data Entry Users')
def story(request, id=None):
    """
    */entry/stories/<id>*, */entry/stories/new*

    The entry interface's edit/add/delete story view. This view creates
    the edit page for a given story, or the "new story" page if it
    is not passed an ID. It also accepts POST requests to create or edit
    stories.

    If called with DELETE, it will return a 200 upon success or a 404 upon
    failure. This is to be used as part of an AJAX call, or some other API
    call.
    """
    if request.method == 'DELETE':
        story = get_object_or_404(Story, pk=id)
        story.delete()
        return HttpResponse()

    if request.method == 'POST':
        message = ''
        post_data = request.POST.copy()

        story_form = StoryForm(post_data)
        if story_form.is_valid():
            image_keys = post_data.get('image_ids', None)
            images = []
            if image_keys:
                images = [Image.objects.get(
                    pk=int(i)) for i in image_keys.split(',')]
            video_keys = post_data.get('video_ids', None)
            videos = []
            if video_keys:
                videos = [Video.objects.get(
                    pk=int(v)) for v in video_keys.split(',')]
            if id:
                story = Story.objects.get(id=id)
                # process images
                existing_images = story.images.all()
                for image in existing_images:
                    if image not in images:
                        story.images.remove(image)
                for image in images:
                    if image not in existing_images:
                        story.images.add(image)
                # process videos
                existing_videos = story.videos.all()
                for video in existing_videos:
                    if video not in videos:
                        story.videos.remove(video)
                for video in videos:
                    if video not in existing_videos:
                        story.videos.add(video)
                story.__dict__.update(**story_form.cleaned_data)
                story.save()
            else:
                story = story_form.save()
                for image in images:
                    story.images.add(image)
                for video in videos:
                    story.videos.add(video)

            return HttpResponseRedirect(
                "%s?success=true" % reverse(
                    'edit-story', kwargs={'id': story.id}))
        else:
            pass
    else:
        message = ''

    if id:
        story = Story.objects.get(id=id)
        title = "Edit {0}".format(story.name)
        post_url = reverse('edit-story', kwargs={'id': id})
        story_form = StoryForm(instance=story)
        existing_images = story.images.all()
        existing_videos = story.videos.all()

        if request.GET.get('success') == 'true':
            message = "Story saved successfully!"

    elif request.method != 'POST':
        story_form = StoryForm()
        post_url = reverse('new-story')
        title = "New Item"
        existing_images = []
        existing_videos = []

    else:
        post_url = reverse('new-story')
        title = "New Item"
        existing_images = []
        existing_videos = []

    data = {'images': [], 'videos': []}

    for image in Image.objects.all():
        data['images'].append({
            'id': image.id,
            'name': image.name
        })

    for video in Video.objects.all():
        data['videos'].append({
            'id': video.id,
            'name': video.name
        })

    return render(request, 'story.html', {
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('entry-list-stories'), 'name': 'Product Education'}
        ],
        'existing_images': existing_images,
        'existing_videos': existing_videos,
        'data_json': json.dumps(data),
        'data_dict': data,
        'title': title,
        'message': message,
        'post_url': post_url,
        'story_form': story_form,
    })
