from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Preparation
from django.contrib.auth.models import User, Group


class InlinePreparationTestCase(TestCase):

    """
    Test that the Inline Preparation popup works as expected.

    Things tested:
        URLs reverse correctly
        The outputted popup has the correct form fields
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
            reverse('edit-product', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/products/1')

    def test_url_endpoint(self):
        url = reverse('preparation_ajax')
        self.assertEqual(url, '/entry/products/new/preparations/new')

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(reverse('preparation_ajax'))

        fields = {'name': 'input', 'description': 'textarea',
                  'additional_info': 'input'}
        form = response.context['preparation_form']

        for field in fields:
            # for the Edit tests, you should be able to access
            # form[field].value
            self.assertIn(fields[field], str(form[field]))

    def test_successful_preparation_creation_minimal(self):
        """
        POST a proper "new preparation" command to the server, and see if the
        new preparation appears in the database. All optional fields are null.
        """
        Preparation.objects.all().delete()

        # Data that we'll post to the server to get the new preparation created
        inline_preparation = {
            'name': 'Fried', 'description': '', 'additional_info': ''}

        self.client.post(reverse('preparation_ajax'), inline_preparation)

        preparation = Preparation.objects.all()[0]
        for field in inline_preparation:
            self.assertEqual(
                getattr(preparation, field), inline_preparation[field])

    def test_successful_preparation_creation_maximal(self):
        """
        POST a proper "new preparation" command to the server, and see if the
        new preparation appears in the database. All optional fields are used.
        """
        Preparation.objects.all().delete()

        # Data that we'll post to the server to get the new preparation created
        inline_preparation = {
            'name': 'Fried',
            'description': 'Test Description',
            'additional_info': 'Fried food is good'}

        self.client.post(reverse('preparation_ajax'), inline_preparation)

        preparation = Preparation.objects.all()[0]
        for field in inline_preparation:
            self.assertEqual(
                getattr(preparation, field), inline_preparation[field])

    def test_no_data_error(self):
        """
        POST a "new preparation" command to the server missing all of the
        required fields, and test to see what the error comes back as.
        """
        # Create a list of all objects before sending bad POST data
        all_preparations = Preparation.objects.all()

        response = self.client.post(reverse('preparation_ajax'))
        required_fields = ['name']
        for field_name in required_fields:
            self.assertIn(field_name,
                          response.context['preparation_form'].errors)

        # Test that we didn't add any new objects
        self.assertEqual(
            list(Preparation.objects.all()), list(all_preparations))
