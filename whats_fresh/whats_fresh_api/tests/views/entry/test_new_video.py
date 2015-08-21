from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Video
from django.contrib.auth.models import User, Group


class NewVideoTestCase(TestCase):

    """
    Test that the New Video page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the creation of a new
            object with the specified details
        POSTing data with all fields missing (hitting "save" without entering
            data) returns the same field with notations of missing fields
    """

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
            reverse('new-video'))
        self.assertRedirects(response, '/login?next=/entry/videos/new')

    def test_url_endpoint(self):
        url = reverse('new-video')
        self.assertEqual(url, '/entry/videos/new')

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(reverse('new-video'))

        fields = {'video': 'input', 'name': 'input', 'caption': 'input'}
        form = response.context['video_form']

        for field in fields:
            # for the Edit tests, you should be able to access
            # form[field].value
            self.assertIn(fields[field], str(form[field]))

    def test_successful_video_creation(self):
        """
        POST a proper "new video" command to the server, and see if the
        new video appears in the database. All optional fields are null.
        """
        Video.objects.all().delete()

        # Data that we'll post to the server to get the new video created
        new_video = {
            'caption': "A thrilling display of utmost might",
            'name': "You won't believe number 3!",
            'video': 'http://www.youtube.com/watch?v=dQw4w9WgXcQ'}

        self.client.post(reverse('new-video'), new_video)

        video = Video.objects.all()[0]
        for field in new_video:
            self.assertEqual(
                getattr(video, field), new_video[field])

    def test_no_data_error(self):
        """
        POST a "new video" command to the server missing all of the
        required fields, and test to see what the error comes back as.
        """
        # Create a list of all objects before sending bad POST data
        all_videos = Video.objects.all()

        response = self.client.post(reverse('new-video'))
        required_fields = ['video']
        for field_name in required_fields:
            self.assertIn(field_name,
                          response.context['video_form'].errors)

        # Test that we didn't add any new objects
        self.assertEqual(
            list(Video.objects.all()), list(all_videos))
