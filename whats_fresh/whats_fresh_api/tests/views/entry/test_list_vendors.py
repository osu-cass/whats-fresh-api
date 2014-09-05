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

        vendor_dict = {}

        for vendor in items:
            vendor_id = vendor['link'].split('/')[-1]
            vendor_dict[str(vendor_id)] = vendor

        for vendor in Vendor.objects.all():
            self.assertEqual(
                vendor_dict[str(vendor.id)]['description'], vendor.description)
            self.assertEqual(
                vendor_dict[str(vendor.id)]['name'], vendor.name)
            self.assertEqual(
                vendor_dict[str(vendor.id)]['link'],
                reverse('edit-vendor', kwargs={'id': vendor.id}))
            self.assertEqual(
                vendor_dict[str(vendor.id)]['modified'],
                vendor.modified.strftime("%I:%M %P, %d %b %Y"))