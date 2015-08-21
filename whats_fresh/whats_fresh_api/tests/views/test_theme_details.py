from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

import json


class ThemeTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)
        self.client.post(
            reverse('login'), {'username': 'test', 'password': 'pass'})

        self.maxDiff = None
        self.expected_theme = """
{
    "error": {
        "status": false,
        "name": null,
        "text": null,
        "debug": null,
        "level": null
    },
    "id": 1,
    "ext": {},
    "name": "Test Name",
    "background_color": "rgb(81, 114, 133)",
    "foreground_color": "rgb(81, 114, 133)",
    "header_color": "rgb(81, 114, 133)",
    "font_color": "rgb(81, 114, 133)",
    "logo": "/media/dog.jpg",
    "slogan": "Test Slogan",
    "site_title": "Oregon Catch",
    "vendors": "shopkeepers",
    "vendors_slug": "vendors",
    "products": "items",
    "products_slug": "products",
    "preparations": "preparations",
    "preparations_slug": "preparations",
    "stories": "stories",
    "stories_slug": "stories",
    "images": "media-image",
    "images_slug": "images",
    "videos": "media-video",
    "videos_slug": "videos",
    "active": "no"
}"""

    def test_url_endpoint(self):
        url = reverse('theme-details', kwargs={'id': '1'})
        self.assertEqual(url, '/1/themes/1')

    def test_theme_endpoint(self):
        response = self.client.get(
            reverse('theme-details', kwargs={'id': '1'})).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.expected_theme)
        self.assertEqual(parsed_answer, expected_answer)
