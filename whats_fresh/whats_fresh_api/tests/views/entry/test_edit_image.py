from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Image
from django.contrib.auth.models import User, Group
import os


class EditImageTestCase(TestCase):

    """
    Test that the Edit Image page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the update of the image
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

        self.test_media_directory = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'testdata', 'media'))

        self.image = open(
            os.path.join(self.test_media_directory, 'cat.jpg'), 'r')

    def test_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse('edit-image', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/images/1')

    def test_url_endpoint(self):
        url = reverse('edit-image', kwargs={'id': '1'})
        self.assertEqual(url, '/entry/images/1')

    def test_successful_image_update(self):
        """
        POST a proper "update image" command to the server, and see if
        the update appears in the database
        """
        # Data that we'll post to the server to get the new image created
        new_image = {
            'caption': "A cat",
            'image': self.image}

        self.client.post(
            reverse('edit-image', kwargs={'id': '1'}),
            new_image)

        image = Image.objects.get(id=1)
        self.assertEqual(getattr(image, 'caption'), new_image['caption'])
        self.assertIn('/media/images/cat', getattr(image, 'image').url)

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(
            reverse('edit-image', kwargs={'id': '2'}))

        fields = {
            'caption': "Meow!",
            'image': self.image}

        form = response.context['image_form']

        self.assertEqual(fields['caption'], form['caption'].value())
        # check that we're displaying the current file in the output
        self.assertIn('/media/cat', response.content)

    def test_delete_image(self):
        """
        Tests that DELETing entry/images/<id> deletes the item
        """
        response = self.client.delete(
            reverse('edit-image', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Image.DoesNotExist):
            Image.objects.get(id=2)

        response = self.client.delete(
            reverse('edit-image', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 404)
