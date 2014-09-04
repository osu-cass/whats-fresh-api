from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class ListPreparationTestCase(TestCase):
    fixtures = ['test_fixtures']

    def test_url_endpoint(self):
        url = reverse('entry-list-preparations')
        self.assertEqual(url, '/entry/preparations')

    def test_list_items(self):
        """
        Tests to see if the list of preparations
        contains the proper preparations
        """
        response = self.client.get(reverse('entry-list-preparations'))
        items = response.context['item_list']

        for preparation in Preparation.objects.all():
            self.assertEqual(
                items[preparation.id-1]['description'],
                preparation.description)
            self.assertEqual(
                items[preparation.id-1]['name'], preparation.name)
            self.assertEqual(
                items[preparation.id-1]['link'],
                reverse('edit-preparation', kwargs={'id': preparation.id}))




