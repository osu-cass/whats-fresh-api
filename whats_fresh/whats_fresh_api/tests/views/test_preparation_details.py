from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class PreparationsTestCase(TestCase):
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
    "name": "Live",
    "description": "The food goes straight from sea to you with live food, sitting in saltwater tanks!",
    "additional_info": "Live octopus requires a locking container"
}"""

    def test_url_endpoint(self):
        url = reverse('preparation-details', kwargs={'id': '1'})
        self.assertEqual(url, '/preparations/1')

    def test_preparation_endpoint(self):
        response = self.client.get(
            reverse('preparation-details', kwargs={'id': '1'})).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_json)
        self.assertEqual(parsed_answer, expected_answer)
