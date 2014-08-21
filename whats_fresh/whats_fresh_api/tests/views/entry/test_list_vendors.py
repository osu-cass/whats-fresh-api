from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class ListVendorTestCase(TestCase):
    fixtures = ['test_fixtures']

    def test_url_endpoint(self):
        url = reverse('new-vendor')
        self.assertEqual(url, '/entry/vendors/new')

    def test_list_items(self):
        """
        Tests to see if the list of vendors contains the proper vendors and
        proper vendor data
        """
        response = self.client.get(reverse('list-vendors-edit'))
        items = response.context['item_list']

        for vendor in Vendor.objects.all():
            self.assertEqual(
                items[vendor.id-1]['description'], vendor.description)
            self.assertEqual(
                items[vendor.id-1]['name'], vendor.name)
            self.assertEqual(
                items[vendor.id-1]['link'],
                reverse('edit-vendor', kwargs={'id': vendor.id}))
            self.assertEqual(
                items[vendor.id-1]['modified'],
                vendor.modified.strftime("%I:%M %P, %d %b %Y"))
