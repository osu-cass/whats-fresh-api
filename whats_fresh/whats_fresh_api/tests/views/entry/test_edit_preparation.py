from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
from django.contrib.auth.models import User
import json


class EditPreparationTestCase(TestCase):
    """
    Test that the Edit Preparation page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the update of the preparation
            object with the specified ID
    """
    fixtures = ['test_fixtures']

    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        user.save()

        self.client.post(
            reverse('login'),
            {'username': 'temporary', 'password': 'temporary'})

    def test_url_endpoint(self):
        url = reverse('edit-preparation', kwargs={'id': '1'})
        self.assertEqual(url, '/entry/preparations/1')

    def test_successful_preparation_update(self):
        """
        POST a proper "update preparation" command to the server, and see if
        the update appears in the database
        """
        # Data that we'll post to the server to get the new preparation created
        new_preparation = {
            'name': u'Fried', 'description': u'', 'additional_info': u''}

        response = self.client.post(
            reverse('edit-preparation', kwargs={'id': '1'}),
            new_preparation)

        preparation = Preparation.objects.get(id=1)
        for field in new_preparation:
            self.assertEqual(
                getattr(preparation, field), new_preparation[field])

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(
            reverse('edit-preparation', kwargs={'id': '1'}))

        fields = {
            'name': u'Fried', 'description': u'', 'additional_info': u''}

        form = response.context['preparation_form']

        for field in fields:
            self.assertEqual(fields[field], form[field].value())
