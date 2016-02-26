from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Image
from django.contrib.auth.models import User, Group
import os


class NewImageTestCase(TestCase):

    """
    Test that the New Image page works as expected.

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

        self.test_media_directory = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'testdata', 'media'))

        self.image = open(
            os.path.join(self.test_media_directory, 'cat.jpg'), 'r')

    def tearDown(self):
        self.image.close()

    def test_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse('new-image'))
        self.assertRedirects(response, '/login?next=/entry/images/new')

    def test_url_endpoint(self):
        url = reverse('new-image')
        self.assertEqual(url, '/entry/images/new')

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(reverse('new-image'))

        fields = {'image': 'file', 'caption': 'input', 'name': 'input'}
        form = response.context['image_form']

        for field in fields:
            # for the Edit tests, you should be able to access
            # form[field].value
            self.assertIn(fields[field], str(form[field]))

    def test_successful_image_creation(self):
        """
        POST a proper "new image" command to the server, and see if the
        new image appears in the database. All optional fields are null.
        """
        Image.objects.all().delete()

        # Data that we'll post to the server to get the new image created
        new_image = {
            'caption': "Catption",
            'name': "A cat",
            'image': self.image}

        self.client.post(reverse('new-image'), new_image)

        image = Image.objects.all()[0]
        self.assertEqual(getattr(image, 'caption'), new_image['caption'])
        self.assertEqual(getattr(image, 'name'), new_image['name'])
        self.assertIn('/media/images/cat', getattr(image, 'image').url)

    def test_no_data_error(self):
        """
        POST a "new image" command to the server missing all of the
        required fields, and test to see what the error comes back as.
        """
        # Create a list of all objects before sending bad POST data
        all_images = Image.objects.all()

        response = self.client.post(reverse('new-image'))
        required_fields = ['image', 'name']
        for field_name in required_fields:
            self.assertIn(field_name,
                          response.context['image_form'].errors)

        # Test that we didn't add any new objects
        self.assertEqual(
            list(Image.objects.all()), list(all_images))
