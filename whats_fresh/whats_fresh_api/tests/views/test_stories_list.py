from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

import json


class StoriesListTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)
        self.client.post(reverse('login'), {'username': 'test',
                                            'password': 'pass'})

        self.maxDiff = None
        self.expected_list = """
{
    "error": {
        "status": false,
        "name": null,
        "text": null,
        "debug": null,
        "level": null
    },
    "stories": [
    {
        "id": 1,
        "name": "Star Wars",
        "history": "A long time ago, in a galaxy far, far away...",
        "facts": "Star Wars is awesome",
        "buying": "Always buy all related products",
        "preparing": "Fried",
        "products": "Fish",
        "season": "Spring",
        "ext": {},
        "images": [
            {"caption": "Woof!", "link": "/media/dog.jpg", "name": "A dog"}
        ],
        "videos": [
            {"caption": "Traveling at the speed of light!", "name": "A Starship",
            "link": "http://www.youtube.com/watch?v=efgDdSWDg0g"}
        ],
        "created": "2014-08-08T23:27:05.568Z",
        "modified": "2014-08-08T23:27:05.568Z"
    }, {
        "id": 2,
        "name": "Fresh Prince",
        "history": "This is the story, all about how my life got flip turned upside down!",
        "facts": "I have never watch this",
        "buying": "Buying people is illegal",
        "preparing": "Being a prince is hard work, make sure you prepare for it",
        "products": "Still illegal",
        "season": "",
        "ext": {},
        "images": [
            {"link": "/media/cat.jpg", "caption": "Meow!", "name": "A cat"}
        ],
        "videos": [
            {"link": "http://www.youtube.com/watch?v=M-nlAuCW7WY",
            "caption": "Princely", "name": "Princely"}
        ],
        "created": "2014-08-08T23:27:05.568Z",
        "modified": "2014-08-08T23:27:05.568Z"
       }
    ]
}
"""

        self.expected_limited_error = """
{
  "error": {
    "status": false,
    "name": null,
    "text": null,
    "debug": null,
    "level": null
  }
}"""

    def test_url_endpoint(self):
        url = reverse('stories-list')
        self.assertEqual(url, '/1/stories')

    def test_no_parameters(self):
        response = self.client.get(reverse('stories-list')).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_list)

        self.maxDiff = None
        self.assertEqual(parsed_answer, expected_answer)

    def test_limited_stories(self):
        response = self.client.get(
            "%s?limit=1" % reverse('stories-list')).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_limited_error)

        self.assertEqual(parsed_answer['error'], expected_answer['error'])
        self.assertEqual(len(parsed_answer['stories']), 1)
