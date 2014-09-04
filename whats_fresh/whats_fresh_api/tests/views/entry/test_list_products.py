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

        for db_product in Product.objects.all():
            list_product = product_dict[str(product.id)]
            self.assertEqual(
                list_product['description'],
                db_product.description)
            self.assertEqual(
                list_product['name'], db_product.name)
            self.assertEqual(
                list_product['link'],
                reverse('edit-product', kwargs={'id': db_product.id}))
            self.assertEqual(
                list_product['modified'],
                db_product.modified.strftime("%I:%M %P, %d %b %Y"))
            self.assertEqual(
                sort(list_product['preparations']),
                sort([prep.name for prep in db_product.preparations.all()]))
