from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Video
from django.contrib.auth.models import User, Group


class EditVideoTestCase(TestCase):

    """
    Test that the Edit Video page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the update of the video
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
            reverse('edit-video', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/videos/1')

    def test_url_endpoint(self):
        url = reverse('edit-video', kwargs={'id': '1'})
        self.assertEqual(url, '/entry/videos/1')

    def test_successful_video_update(self):
        """
        POST a proper "update video" command to the server, and see if
        the update appears in the database
        """
        # Data that we'll post to the server to get the new video created
        new_video = {
            'caption': "A thrilling display of utmost might",
            'video': 'http://www.youtube.com/watch?v=dQw4w9WgXcQ'}

        self.client.post(
            reverse('edit-video', kwargs={'id': '1'}),
            new_video)

        video = Video.objects.get(id=1)
        for field in new_video:
            self.assertEqual(
                getattr(video, field), new_video[field])

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(
            reverse('edit-video', kwargs={'id': '1'}))

        fields = {
            'caption': 'A Starship',
            'video': 'http://www.youtube.com/watch?v=efgDdSWDg0g'
        }

        form = response.context['video_form']

        for field in fields:
            self.assertEqual(fields[field], form[field].value())

    def test_delete_video(self):
        """
        Tests that DELETing entry/videos/<id> deletes the item
        """
        response = self.client.delete(
            reverse('edit-video', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Video.DoesNotExist):
            Video.objects.get(id=2)

        response = self.client.delete(
            reverse('edit-video', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 404)
