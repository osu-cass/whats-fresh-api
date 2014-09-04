from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class NewPreparationTestCase(TestCase):
    """
    Test that the New Preparation page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the creation of a new
            object with the specified details
        POSTing data with all fields missing (hitting "save" without entering
            data) returns the same field with notations of missing fields
    """
    def test_url_endpoint(self):
        url = reverse('new-preparation')
        self.assertEqual(url, '/entry/preparations/new')

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(reverse('new-preparation'))

        fields = {'name': 'input', 'description': 'input',
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
        new_preparation = {
            'name': 'Fried', 'description': '', 'additional_info': ''}

        response = self.client.post(reverse('new-preparation'),
                                    new_preparation)

        preparation = Preparation.objects.all()[0]
        for field in new_preparation:
            self.assertEqual(
                getattr(preparation, field), new_preparation[field])

    def test_successful_preparation_creation_maximal(self):
        """
        POST a proper "new preparation" command to the server, and see if the
        new preparation appears in the database. All optional fields are used.
        """
        Preparation.objects.all().delete()

        # Data that we'll post to the server to get the new preparation created
        new_preparation = {
            'name': 'Fried',
            'description': 'Test Description',
            'additional_info': 'Fried food is good'}

        response = self.client.post(reverse('new-preparation'),
                                    new_preparation)

        preparation = Preparation.objects.all()[0]
        for field in new_preparation:
            self.assertEqual(
                getattr(preparation, field), new_preparation[field])

    def test_no_data_error(self):
        """
        POST a "new preparation" command to the server missing all of the
        required fields, and test to see what the error comes back as.
        """
        # Create a list of all objects before sending bad POST data
        all_preparations = Preparation.objects.all()

        response = self.client.post(reverse('new-preparation'))
        required_fields = ['name']
        for field_name in required_fields:
            self.assertIn(field_name,
                          response.context['preparation_form'].errors)

        # Test that we didn't add any new objects
        self.assertEqual(
            list(Preparation.objects.all()), list(all_preparations))

