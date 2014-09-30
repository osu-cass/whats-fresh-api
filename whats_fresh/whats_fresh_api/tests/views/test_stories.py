from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

import json


class StoriesTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)
        self.client.post(reverse('login'), {'username': 'test',
                                            'password': 'pass'})

        self.maxDiff = None

        self.expected_json = """
{
    "error": {
        "status": false,
        "name": null,
        "text": null,
        "debug": null,
        "level": null
    },
    "story": "These are the voyages of the Starfish Enterblub; her five year\
 mission -- to seek out new fish and new fishilizations..."
    "id": 1,
    "name": "Star Wars",
    "history": "A long time ago, in a galaxy far, far away...",
    "facts": "Star Wars is awesome",
    "buying": "I have no idea what this field is for.",
    "preparing": "Fried",
    "products": "Fish",
    "season": "Spring",
    "created": "2014-08-08 23:27:05.568395+00:00",
    "modified": "2014-08-08 23:27:05.568395+00:00"
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
        self.assertEqual(url, '/1/stories/1')

    def test_known_story(self):
        response = self.client.get(
            reverse('story-details', kwargs={'id': '1'})).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_json)
        self.assertEqual(parsed_answer, expected_answer)

    def test_story_items(self):
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
        self.assertEqual(parsed_answer, expected_answer)
