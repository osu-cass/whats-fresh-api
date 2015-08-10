from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Theme
from django.contrib.auth.models import User, Group


class NewThemeTestCase(TestCase):

    """
    Test that the New Theme works as expected.

    Things tested:
        URLs reverse correctly
        The page has the correct form fields
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
            reverse('edit-theme', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/admin/theme/1')

    def test_url_endpoint(self):
        url = reverse('new-theme')
        self.assertEqual(url, '/admin/whats_fresh_api/theme/add/')

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.post(
            reverse('login'),
            {'username': 'temporary', 'password': 'temporary'})
        response = self.client.get(reverse('new-theme'))

        fields = {'name': 'input', 'background_color': 'input',
                  'foreground_color': 'input', 'logo': 'file',
                  'slogan': 'input', 'site_title': 'input',
                  'vendors': 'input', 'vendors_slug': 'input',
                  'products': 'input', 'products_slug': 'input',
                  'preparations': 'input', 'preparations_slug': 'input',
                  'stories': 'input', 'stories_slug': 'input',
                  'images': 'input', 'images_slug': 'input',
                  'videos': 'input', 'videos_slug': 'input', 'active': 'input'
                  }
        form = response.context['theme_form']

        for field in fields:
            # for the Edit tests, you should be able to access
            # form[field].value
            self.assertIn(fields[field], str(form[field]))

    def test_successful_theme_creation(self):
        """
        POST a proper "new theme" and see if the
        new theme appears in the database
        """
        self.client.post(reverse('login'),
                         {'username': 'temporary', 'password': 'temporary'})

        # We can't predict what the ID of the new theme will be, so we can
        # delete all of the themes, and then choose the only theme left
        # after creation.
        Theme.objects.all().delete()

        # Data that we'll post to the server to get the new theme created
        new_theme = {
            'zip': '97365', 'website': '', 'hours': 'optional hours',
            'street': '750 NW Lighthouse Dr', 'story': '',
            'status': '', 'state': 'OR', 'preparation_ids': '1,2',
            'phone': '', 'name': 'Test Name',
            'latitude': '44.6752643', 'longitude': '-124.072162',
            'location_description': 'Optional Description',
            'email': '', 'description': 'Test Description',
            'contact_name': 'Test Contact', 'city': 'Newport'}

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

        self.client.post(reverse('new-theme'), new_theme)

        self.assertGreater(len(Theme.objects.all()), 0)

        them = Theme.objects.all()[0]
        for field in new_theme:
            self.assertEqual(getattr(them, field), new_theme[field])

    def test_no_data_error(self):
        """
        POST a "new theme" command to the server missing all of the
        required fields, and test to see what the error comes back as.
        """
        response = self.client.post(
            reverse('login'),
            {'username': 'temporary', 'password': 'temporary'})
        # Create a list of all objects before sending bad POST data
        all_themes = Theme.objects.all()

        new_theme = {
            'name': '', 'background_color': '',
            'foreground_color': '', 'site_title': '',
            'vendors': '', 'vendors_slug': '',
            'products': '', 'products_slug': '',
            'preparations': '', 'preparations_slug': '',
            'stories': '', 'stories_slug': '',
            'images': '', 'images_slug': '',
            'videos': '', 'videos_slug': ''
        }

        response = self.client.post(reverse('new-theme'), new_theme)

        # Test non-automatically generated errors written into the view

        required_fields = [
            'site_title', 'name', 'vendors', 'vendors_slug', 'products',
            'products_slug', 'preparations', 'preparations_slug',
            'stories', 'stories_slug', 'images', 'images_slug',
            'videos', 'videos_slug']
        for field_name in required_fields:
            self.assertIn(field_name, response.context['theme_form'].errors)

        # Test that we didn't add any new objects
        self.assertTrue(list(Theme.objects.all()) == list(all_themes))
