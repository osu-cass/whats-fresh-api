from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Theme
from django.contrib.auth.models import User, Group


class EditThemeTestCase(TestCase):

    """
    Test that the Edit Theme page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the update of the vendor
            object with the specified ID
        POSTing data with all fields missing (hitting "save" without entering
            data) returns the same field with notations of missing fields
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
            reverse('edit-theme', kwargs={'id': '1'}))
        self.assertRedirects(
            response, '/login?next=/admin/whats_fresh_api/theme/1')

    def test_url_endpoint(self):
        url = reverse('edit-theme', kwargs={'id': '1'})
        self.assertEqual(url, '/admin/whats_fresh_api/theme/1')

    def test_successful_theme_update(self):
        """
        POST a proper "new theme" command to the server, and see if the
        new theme appears in the database
        """

        # Data that we'll post to the server to get the new theme created
        new_theme = {'name': 'Test Name',
                     'background_color': 'rgb(81, 114, 133)',
                     'foreground_color': 'rgb(81, 114, 133)',
                     'logo': self.logo, 'slogan': 'Test Slogan',
                     'site_title': 'Oregon Catch',
                     'vendors': 'vendors', 'vendors_slug': 'vendors',
                     'products': 'products', 'products_slug': 'products',
                     'preparations': 'preparations',
                     'preparations_slug': 'preparations',
                     'stories': 'stories', 'stories_slug': 'stories',
                     'images': 'images', 'images_slug': 'images',
                     'videos': 'videos', 'videos_slug': 'videos',
                     'active': 'no'
                     }

        self.client.post(
            reverse('edit-theme', kwargs={'id': '1'}), new_theme)

        them = Theme.objects.get(id=1)
        for field in new_theme:
            self.assertEqual(getattr(them, field), new_theme[field])

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields with the
        right initial data
        """

        response = self.client.get(reverse('edit-theme', kwargs={'id': '1'}))

        fields = {
            'name': "Test Name",
            'background_color': "rgb(81, 114, 133)",
            'foreground_color': "rgb(81, 114, 133)",
            'logo': self.logo,
            'slogan': "Test Slogan",
            'site_title': "Oregon Catch",
            'vendors': "vendors",
            'vendors_slug': "vendors",
            'products': "products",
            'products_slug': "products",
            'preparations': "preparations",
            'preparations_slug': "preparations",
            'stories': "stories",
            'stories_slug': "stories",
            'images': "images",
            'images_slug': "images",
            'videos': "videos",
            'videos_slug': "videos",
            'active': "no"
        }

        form = response.context['theme_form']

        for field in fields:
            self.assertEqual(fields[field], form[field].value())
