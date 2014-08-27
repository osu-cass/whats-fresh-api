from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class VendorsTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        self.expected_json = """
{
  "error": {
    "error_status": false,
    "error_name": null,
    "error_text": null,
    "error_level": null
  },
  "vendors": [
    {
      "id": 1,
      "name": "No Optional Null Fields Are Null",
      "status": true,
      "description": "This is a vendor shop.",
      "lat": 37.833688,
      "long": -122.478002,
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
      "story": 1,
      "ext": {
        
      },
      "created": "2014-08-08 23:27:05.568395+00:00",
      "updated": "2014-08-08 23:27:05.568395+00:00",
      "products": [
        {
          "id": 2,
          "name": "Starfish Voyager",
          "preparation": "Live"
        },
        {
          "id": 1,
          "name": "Ezri Dax",
          "preparation": "Live"
        }
      ]
    },
{
 "id": 2,
        "name": "All Optional Null Fields Are Null",
        "status": null,
        "description": "Ceci n'est pas un magasin.",
        "lat": 43.418297,
        "long": -124.219635,
        "street": "501 Isabelle Rd",
        "city": "North Bend",
        "state": "OR",
        "zip": "97459",
        "location_description": "",
        "contact_name": "Isabelle",
        "phone": null,
        "hours": "",
        "website": "",
        "email": "",
        "story": null,
        "ext": {},
        "created": "2014-08-08 23:27:05.568395+00:00",
        "updated": "2014-08-08 23:27:05.568395+00:00",
        "products": [
            {
                "id": 1,
                "name": "Ezri Dax",
                "preparation": "Live"
            }
        ]
    }

  ]
}
"""

    def test_url_endpoint(self):
        url = reverse('vendors-list')
        self.assertEqual(url, '/vendors')

    def test_json_equals(self):
        c = Client()
        response = c.get(reverse('vendors-list')).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_json)

        for vendor in expected_answer['vendors']:
            vendor['products'] = sorted(
                vendor['products'], key=lambda k: k['id'])

        for vendor in parsed_answer['vendors']:
            vendor['products'] = sorted(
                vendor['products'], key=lambda k: k['id'])

        parsed_answer['vendors'] = sorted(
            parsed_answer['vendors'], key=lambda k: k['id'])
        expected_answer['vendors'] = sorted(
            expected_answer['vendors'], key=lambda k: k['id'])

        self.maxDiff = None
        self.assertEqual(parsed_answer, expected_answer)
