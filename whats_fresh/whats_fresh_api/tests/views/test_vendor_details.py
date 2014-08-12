from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class StoriesTestCase(TestCase):
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
  "name": "No Optional Null Fields Are Null",
  "status": true,
  "description": "This is a vendor shop.",
  "lat": 37.833688,
  "long": -122.478002,
  "street": "1633 Sommerville Rd",
  "city": "Sausalito",
  "state": "CA",
  "zip": "94965",
  "location_description": "Location description",
  "contact_name": "A. Persson",
  "phone": 5417377627,
  "website": "http://example.com",
  "email": "a@perr.com",
  "story": 1,
  "ext": {},
  "created": "2014-08-08 23:27:05.568395+00:00",
  "updated": "2014-08-08 23:27:05.568395+00:00",
  "products": {
    "1": {
      "name": "Starfish Voyager",
      "preparation": "Live"
    },
    "2": {
      "name": "Ezri Dax",
      "preparation": "Live"
    }
  }
}"""

    def test_url_endpoint(self):
       url = reverse('vendor-details', kwargs={'id': '1'})
       self.assertEqual(url, '/vendors/1')

    def test_json_equals(self):
        c = Client()
        response = c.get(reverse('vendor-details', kwargs={'id': '1'})).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_json)
        self.assertTrue(parsed_answer == expected_answer)
