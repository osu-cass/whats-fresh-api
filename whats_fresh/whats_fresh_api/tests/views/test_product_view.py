from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

import json


class ProductViewTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)
        self.client.post(
            reverse('login'), {'username': 'test', 'password': 'pass'})

        self.expected_list = """
{
  "error": {
    "status": false,
    "name": null,
    "text": null,
    "debug": null,
    "level": null
  },
  "products": [
    {
      "id": 2,
      "name": "Starfish Voyager",
      "variety": "Tuna",
      "alt_name": "The Stargazer",
      "description": "This is one sweet fish!",
      "origin": "The Delta Quadrant",
      "season": "Season 1",
      "available": true,
      "market_price": "$33.31",
      "link": "http://www.amazon.com/Star-Trek-Voyager-\
Complete-Seventh/dp/B00062IDCO/",
      "image": {"caption": "Woof!", "link": "/media/dog.jpg"},
      "story": 1,
      "created": "2014-08-08T23:27:05.568Z",
      "modified": "2014-08-08T23:27:05.568Z",
      "ext": {}
    },
    {
      "id": 1,
      "name": "Ezri Dax",
      "variety": "Freshwater Eel",
      "alt_name": "Jadzia",
      "description": "That's not actually an eel, it's a symbiote.",
      "origin": "Trill",
      "season": "Season 7",
      "available": true,
      "market_price": "$32.64 per season",
      "link": "http://www.amazon.com/Star-Trek-Deep-Space-Nine/dp/B00008KA57/",
      "image": {"caption": "Meow!", "link": "/media/cat.jpg"},
      "story": 2,
      "created": "2014-08-08T23:27:05.568Z",
      "modified": "2014-08-08T23:27:05.568Z",
      "ext": {}
    }
  ]
}"""

        self.limited_products_error = """
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
        url = reverse('products-list')
        self.assertEqual(url, '/1/products')

    def test_products_list(self):
        response = self.client.get(reverse('products-list')).content
        parsed_answer = json.loads(response)
        expected_answer = json.loads(self.expected_list)

        parsed_answer['products'] = sorted(
            parsed_answer['products'], key=lambda k: k['id'])
        expected_answer['products'] = sorted(
            expected_answer['products'], key=lambda k: k['id'])

        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)

    def test_limited_products(self):
        response = self.client.get(
            "%s?limit=1" % reverse('products-list')).content
        parsed_answer = json.loads(response)

        expected_answer = json.loads(self.limited_products_error)

        self.assertEqual(parsed_answer['error'], expected_answer['error'])
        self.assertEqual(len(parsed_answer['products']), 1)


class NoProductViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)
        self.client.post(
            reverse('login'), {'username': 'test', 'password': 'pass'})

        self.expected_no_products = """
{
  "error": {
    "status": true,
    "text": "No Products found",
    "name": "No Products",
    "debug": "",
    "level": "Error"
  },
  "products": []
}"""

    def test_no_products(self):
        response = self.client.get(reverse('products-list'))
        parsed_answer = json.loads(response.content)
        expected_answer = json.loads(self.expected_no_products)
        self.assertEqual(response.status_code, 200)

        self.maxDiff = None

        self.assertEqual(parsed_answer, expected_answer)
