from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from whats_fresh_api.models import *
from django.contrib.gis.db import models

import json

class ProductVendorTestCase(TestCase):
    fixtures = ['whats_fresh_api/tests/testdata/test_fixtures.json']

    def setUp(self):
        self.expected_json = """
        {
            "error": {
                "error_status": false,
                "error_name": null,
                "error_text": null,
                "error_level": null
            },
            "2": {
                "name": "Starfish Voyager",
                "variety": "Tuna",
                "alt_name": "The Stargazer",
                "description": "This is one sweet fish!",
                "origin": "The Delta Quadrant",
                "season": "Season 1",
                "available": true,
                "market_price": "$33.31",
                "link": "http://www.amazon.com/Star-Trek-Voyager-Complete-Seventh/dp/B00062IDCO/",
                "image": "/media/dog.jpg",
                "story_id": 1,
                "id": 2,
                "created": "2014-08-08 23:27:05.568395+00:00",
                "modified": "2014-08-08 23:27:05.568395+00:00"
            },
            "1": {
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
                "story_id": 2,
                "id": 1,
                "created": "2014-08-08 23:27:05.568395+00:00",
                "modified": "2014-08-08 23:27:05.568395+00:00"
            }
        }"""

    def test_url_endpoint(self):
        url = reverse('product-vendor', kwargs={'id': '1'})
        self.assertEqual(url, '/products/vendors/1')

    def test_json_equals(self):
        c = Client()
        response = c.get(reverse('product-vendor', kwargs={'id': '1'})).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_json)
        self.assertTrue(parsed_answer == expected_answer)
