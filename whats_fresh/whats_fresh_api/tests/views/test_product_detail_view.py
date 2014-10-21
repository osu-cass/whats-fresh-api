from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User, Group, Permission

from whats_fresh.whats_fresh_api.models import *
from django.contrib.gis.db import models

import os
import time
import sys
import datetime
import json


class ProductViewTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)
        self.client.post(reverse('login'), {'username':'test', 'password':'pass'})

        self.expected_product = """
{
  "error": {
    "status": false,
    "name": null,
    "text": null,
    "debug": null,
    "level": null
  },
  "id": 1,
  "name": "Ezri Dax",
  "variety": "Freshwater Eel",
   "alt_name": "Jadzia",
  "description": "That's not actually an eel, it's a symbiote.",
  "origin": "Trill",
  "season": "Season 7",
  "available": true,
  "market_price": "$32.64 per season",
  "link": "http://www.amazon.com/Star-Trek-Deep-Space-Nine/dp/B00008KA57/",
  "image": "/media/cat.jpg",
  "story": 2,
  "created": "2014-08-08 23:27:05.568395+00:00",
  "modified": "2014-08-08 23:27:05.568395+00:00"
}"""

        self.expected_not_found = """
{
  "error": {
    "status": true,
    "text": "Product id 999 was not found.",
    "name": "Product Not Found",
    "debug": "DoesNotExist: Product matching query does not exist.",
    "level": "Error"
  }
}"""

    def test_url_endpoint(self):
        url = reverse('product-details', kwargs={'id': '1'})
        self.assertEqual(url, '/1/products/1')

    def test_known_product(self):
        response = self.client.get(
            reverse('product-details', kwargs={'id': '1'}))

        parsed_answer = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

        expected_answer = json.loads(self.expected_product)
        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)

    def test_product_not_found(self):
        response = self.client.get(
            reverse('product-details', kwargs={'id': '999'}))
        parsed_answer = json.loads(response.content)
        self.assertEqual(response.status_code, 404)

        expected_answer = json.loads(self.expected_not_found)
        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)
