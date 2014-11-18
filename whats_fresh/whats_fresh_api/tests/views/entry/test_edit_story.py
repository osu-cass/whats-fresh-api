from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Story, Image, Video
from django.contrib.auth.models import User, Group


class EditStoryTestCase(TestCase):

    """
    Test that the Edit Story page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the update of the story
            object with the specified ID
    """
    fixtures = ['test_fixtures']

    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        user.save()

        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)

        response = self.client.login(
            username='temporary', password='temporary')
        self.assertEqual(response, True)

    def test_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse('edit-story', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/stories/1')

    def test_url_endpoint(self):
        url = reverse('edit-story', kwargs={'id': '1'})
        self.assertEqual(url, '/entry/stories/1')

    def test_successful_story_update(self):
        """
        POST a proper "update story" command to the server, and see if
        the update appears in the database
        """
        # Data that we'll post to the server to get the new story created
        new_story = {'name': 'To The Moon!', 'history': '',
                     'facts': '', 'buying': '',
                     'preparing': '', 'products': '',
                     'season': '', 'image_ids': '1',
                     'video_ids': '2'}

        self.client.post(
            reverse('edit-story', kwargs={'id': '1'}),
            new_story)
        del new_story['image_ids']
        del new_story['video_ids']

        story = Story.objects.get(id=1)
        for field in new_story:
            self.assertEqual(
                getattr(story, field), new_story[field])

        images = ([image.id for image in story.images.all()])
        self.assertEqual(sorted(images), [1])

        videos = ([video.id for video in story.videos.all()])
        self.assertEqual(sorted(videos), [2])

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(
            reverse('edit-story', kwargs={'id': '1'}))

        fields = {
            "name": "Star Wars",
            "history": "A long time ago, in a galaxy far, far away...",
            "facts": "Star Wars is awesome",
            "buying": "Always buy all related products",
            "preparing": "Fried",
            "products": "Fish",
            "season": "Spring"
        }

        form = response.context['story_form']

        for field in fields:
            self.assertEqual(fields[field], form[field].value())

    def test_delete_story(self):
        """
        Tests that DELETing entry/stories/<id> deletes the item
        """
        response = self.client.delete(
            reverse('edit-story', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Story.DoesNotExist):
            Story.objects.get(id=2)

        response = self.client.delete(
            reverse('edit-story', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 404)
