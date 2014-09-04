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
        Tests to see if the list of preparations contains the proper preparations and
        proper preparation data
        """
        response = self.client.get(reverse('entry-list-preparations'))
        items = response.context['item_list']

        preparation_dict = {}

        for preparation in items:
            preparation_id = preparation['link'].split('/')[-1]
            preparation_dict[str(preparation_id)] = preparation

        for db_preparation in Preparation.objects.all():
            list_preparation = preparation_dict[str(db_preparation.id)]
            self.assertEqual(
                list_preparation['description'], db_preparation.description)
            self.assertEqual(
                list_preparation['name'], db_preparation.name)
            self.assertEqual(
                list_preparation['link'],
                reverse('edit-preparation', kwargs={'id': db_preparation.id}))
