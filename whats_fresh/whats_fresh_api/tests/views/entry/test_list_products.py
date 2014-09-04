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
        Tests to see if the list of products contains the proper products and
        proper product data
        """
        response = self.client.get(reverse('entry-list-products'))
        items = response.context['item_list']

        product_dict = {}

        for product in items:
            product_id = product['link'].split('/')[-1]
            product_dict[str(product_id)] = product

        for product in Product.objects.all():
            self.assertEqual(
                product_dict[str(product.id)]['description'],
                product.description)
            self.assertEqual(
                product_dict[str(product.id)]['name'], product.name)
            self.assertEqual(
                product_dict[str(product.id)]['link'],
                reverse('edit-product', kwargs={'id': product.id}))
            self.assertEqual(
                product_dict[str(product.id)]['modified'],
                product.modified.strftime("%I:%M %P, %d %b %Y"))
            self.assertEqual(
                sort(product_dict[str(product.id)]['preparations']),
                sort([prep.name for prep in product.preparations.all()]))
