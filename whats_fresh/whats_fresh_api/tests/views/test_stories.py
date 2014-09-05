from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class StoriesTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        self.expected_json = """
{
    "error": {
        "status": false,
        "name": null,
        "text": null,
        "debug": null,
        "level": null
    },
    "story": "These are the voyages of the Starfish Enterblub; her five year mission -- to seek out new fish and new fishilizations..."
}"""

        self.expected_not_found = """
{
  "error": {
    "status": true,
    "text": "Story id 999 was not found.",
    "name": "Story Not Found",
    "debug": "DoesNotExist: Story matching query does not exist.",
    "level": "Error"
  }
}"""

    def test_url_endpoint(self):
        url = reverse('story-details', kwargs={'id': '1'})
        self.assertEqual(url, '/stories/1')

    def test_known_story(self):
        response = self.client.get(
            reverse('story-details', kwargs={'id': '1'})).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_json)
        self.assertEqual(parsed_answer, expected_answer)

    def test_story_not_found(self):
        response = self.client.get(
            reverse('story-details', kwargs={'id': '999'}))
        parsed_answer = json.loads(response.content)
        self.assertEqual(response.status_code, 404)

        expected_answer = json.loads(self.expected_not_found)
        self.maxDiff = None
        self.assertEqual(parsed_answer, expected_answer)
