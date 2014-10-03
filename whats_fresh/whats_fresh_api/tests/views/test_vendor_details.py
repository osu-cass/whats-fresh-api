from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class VendorTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        self.expected_vendor = """
{
  "error": {
    "status": false,
    "name": null,
    "text": null,
    "debug": null,
    "level": null
  },
  "name": "No Optional Null Fields Are Null",
  "status": true,
  "description": "This is a vendor shop.",
  "lat": 37.833688,
  "lng": -122.478002,
  "street": "1633 Sommerville Rd",
  "city": "Sausalito",
  "state": "CA",
  "zip": "94965",
  "hours": "Open Tuesday, 10am to 5pm",
  "location_description": "Location description",
  "contact_name": "A. Persson",
  "phone": 5417377627,
  "website": "http://example.com",
  "email": "a@perr.com",
  "story_id": 1,
  "ext": {},
  "id": 1,
  "created": "2014-08-08 23:27:05.568395+00:00",
  "updated": "2014-08-08 23:27:05.568395+00:00",
  "products": [
    {
      "product_id": 2,
      "preparation_id": 1,
      "name": "Starfish Voyager",
      "preparation": "Live"
    },
    {
      "product_id": 1,
      "preparation_id": 1,
      "name": "Ezri Dax",
      "preparation": "Live"
    }
  ]
}"""

        self.expected_not_found = """
{
  "error": {
    "status": true,
    "text": "Vendor id 999 was not found.",
    "name": "Vendor Not Found",
    "debug": "DoesNotExist: Vendor matching query does not exist.",
    "level": "Error"
  }
}"""

    def test_url_endpoint(self):
        url = reverse('vendor-details', kwargs={'id': '1'})
        self.assertEqual(url, '/1/vendors/1')

    def test_known_vendor(self):
        response = self.client.get(
            reverse('vendor-details', kwargs={'id': '1'})).content

        parsed_answer = json.loads(response)
        expected_answer = json.loads(self.expected_vendor)

        self.maxDiff = None
        self.assertEqual(parsed_answer, expected_answer)

    def test_vendor_not_found(self):
        response = self.client.get(
            reverse('vendor-details', kwargs={'id': '999'}))
        self.assertEqual(response.status_code, 404)

        parsed_answer = json.loads(response.content)
        expected_answer = json.loads(self.expected_not_found)

        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)
