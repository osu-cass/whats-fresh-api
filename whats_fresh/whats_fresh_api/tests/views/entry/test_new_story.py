from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Story
from django.contrib.auth.models import User, Group


class NewStoryTestCase(TestCase):

    """
    Test that the New Story page works as expected.

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
            reverse('edit-story', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/stories/1')

    def test_url_endpoint(self):
        url = reverse('new-story')
        self.assertEqual(url, '/entry/stories/new')

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(reverse('new-story'))

        fields = {'name': 'input', 'history': 'textarea',
                  'facts': 'textarea', 'buying': 'textarea',
                  'preparing': 'textarea', 'products': 'textarea',
                  'season': 'textarea'}

        form = response.context['story_form']

        for field in fields:
            # for the Edit tests, you should be able to access
            # form[field].value
            self.assertIn(fields[field], str(form[field]))

    def test_successful_story_creation_minimal(self):
        """
        POST a proper "new story" command to the server, and see if the
        new story appears in the database. All optional fields are null.
        """
        Story.objects.all().delete()

        # Data that we'll post to the server to get the new story created
        new_story = {'name': 'To The Moon!', 'history': '',
                     'facts': '', 'buying': '',
                     'preparing': '', 'products': '',
                     'season': ''}

        self.client.post(reverse('new-story'), new_story)

        story = Story.objects.all()[0]
        for field in new_story:
            self.assertEqual(
                getattr(story, field), new_story[field])

    def test_successful_story_creation_maximal(self):
        """
        POST a proper "new story" command to the server, and see if the
        new story appears in the database. All optional fields are used.
        """
        Story.objects.all().delete()

        # Data that we'll post to the server to get the new story created
        new_story = {'name': 'To The Moon!',
                     'history': 'Dogecoin was introduced in December 2013',
                     'facts': 'Dogecoin is awesome!',
                     'buying': 'As a cryptocurrency, Dogecoin can be mined',
                     'preparing': 'Just mine some and use it!',
                     'products': 'Accepted anywhere on the moon',
                     'season': 'All the time'}

        self.client.post(reverse('new-story'), new_story)

        story = Story.objects.all()[0]
        for field in new_story:
            self.assertEqual(
                getattr(story, field), new_story[field])

    def test_no_data_error(self):
        """
        POST a "new story" command to the server missing all of the
        required fields, and test to see what the error comes back as.
        """
        # Create a list of all objects before sending bad POST data
        all_stories = Story.objects.all()

        response = self.client.post(reverse('new-story'))
        required_fields = ['name']
        for field_name in required_fields:
            self.assertIn(field_name,
                          response.context['story_form'].errors)

        # Test that we didn't add any new objects
        self.assertEqual(
            list(Story.objects.all()), list(all_stories))
