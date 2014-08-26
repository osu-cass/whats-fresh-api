from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class ListProductTestCase(TestCase):
    fixtures = ['test_fixtures']

    def test_url_endpoint(self):
        url = reverse('entry-list-products')
        self.assertEqual(url, '/entry/products')

    def test_list_items(self):
        """
        Tests to see if the list of products contains the proper productss and
        proper product data
        """
        response = self.client.get(reverse('entry-list-products'))
        items = response.context['item_list']

        for product in Product.objects.all():
            self.assertEqual(
                items[product.id-1]['description'], product.description)
            self.assertEqual(
                items[product.id-1]['name'], product.name)
            self.assertEqual(
                items[product.id-1]['link'],
                reverse('edit-product', kwargs={'id': product.id}))
            self.assertEqual(
                items[product.id-1]['modified'],
                product.modified.strftime("%I:%M %P, %d %b %Y"))
            self.assertEqual(
                sort(items[product.id-1]['preparations']),
                sort([prep.name for prep in product.preparations.all()])

