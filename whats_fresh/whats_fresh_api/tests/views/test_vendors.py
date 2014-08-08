from django.test import TestCase
from django.core import management
from django.test.client import Client
from django.core.urlresolvers import reverse

from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class VendorsTestCase(TestCase):
    def setUp(self):
        """
        Install fixtures and define initial expected JSON
        """
        management.call_command('loaddata', 'fixtures', verbosity=0)

        # This is the expected return, as JSON
        # We can't use this, unfortunately, because we nede to allow
        # for 'created' and 'updated' to be changed
        self.expected_json = """
{
    "error": {
        "error_status": false,
        "error_name": null,
        "error_text": null,
        "error_level": null
    },
    "1": {
        "name": "No Optional Null Fields Are Null",
        "status": true,
        "description": "This is a vendor shop.",
        "lat": "37.833688000000002",
        "long": "-122.478002",
        "street": "1633 Sommerville Rd",
        "city": "Sausalito",
        "state": "CA",
        "zip": "94965",
        "location_description": "Location description",
        "contact_name": "A. Persson",
        "phone": "5417377627",
        "website": "http://example.com",
        "email": "a@perr.com",
        "story": "1",
        "ext": {},
        "created": "known string",
        "updated": "known string",
        "products": {
            "1": {
                "name": "Starfish Voyager",
                "preparation": "Live"
            },
            "2": {
                "name": "Something",
                "preparation": "Live"
            }
        }
    },
    "2": {
        "name": "All Optional Null Fields Are Null",
        "status": null,
        "description": "Ceci n'est pas un magasin.",
        "lat": "43.418297000000003",
        "long": "-124.219635",
        "street": "501 Isabelle Rd",
        "city": "North Bend",
        "state": "OR",
        "zip": "97459",
        "location_description": null,
        "contact_name": "Isabelle",
        "phone": null,
        "website": null,
        "email": null,
        "story": null,
        "ext": {},
        "created": "known string",
        "updated": "known string",
        "products": {
            "1": {
                "name": "Starfish Voyager",
                "preparation": "Live"
            }
        }
    }
}"""


    def test_url_endpoint(self):
        url = reverse('vendors-list')
        self.assertEqual(url, '/vendors')

    def test_json_equals(self):
        c = Client()
        response = c.get(reverse('vendors-list')).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_json)

        # Set created and updated to known strings
        for dictionary in [parsed_answer, expected_answer]:
            for first_key in ['1', '2']:
                for second_key in ['created', 'updated']:
                    dictionary[first_key][second_key] = "known string"

        self.assertTrue(parsed_answer['1'] == expected_answer['1'])
        self.assertTrue(parsed_answer['2'] == expected_answer['2'])
        self.assertTrue(parsed_answer['error'] == expected_answer['error'])
