from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

import json


class ProductVendorTestCase(TestCase):
    fixtures = ['test_fixtures']

    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)
        self.client.post(
            reverse('login'), {'username': 'test', 'password': 'pass'})

        self.maxDiff = None
        self.expected_products = """
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
      "ext": {},
      "name": "Starfish Voyager",
      "variety": "Tuna",
      "alt_name": "The Stargazer",
      "description": "This is one sweet fish!",
      "origin": "The Delta Quadrant",
      "season": "Season 1",
      "available": true,
      "market_price": "$33.31",
      "link": "http://www.amazon.com/Star-Trek-\
Voyager-Complete-Seventh/dp/B00062IDCO/",
      "image": {"caption": "Woof!", "link": "/media/dog.jpg", "name": "A dog"},
      "story": 1,
      "created": "2014-08-08T23:27:05.568Z",
      "modified": "2014-08-08T23:27:05.568Z"
    },
    {
      "id": 1,
      "ext": {},
      "name": "Ezri Dax",
      "variety": "Freshwater Eel",
      "alt_name": "Jadzia",
      "description": "That's not actually an eel, it's a symbiote.",
      "origin": "Trill",
      "season": "Season 7",
      "available": true,
      "market_price": "$32.64 per season",
      "link": "http://www.amazon.com/Star-Trek-Deep-Space-Nine/dp/B00008KA57/",
      "image": {"caption": "Meow!", "link": "/media/cat.jpg", "name": "A cat"},
      "story": 2,
      "created": "2014-08-08T23:27:05.568Z",
      "modified": "2014-08-08T23:27:05.568Z"
    }
  ]
}"""

    def test_url_endpoint(self):
        url = reverse('product-vendor', kwargs={'id': '1'})
        self.assertEqual(url, '/1/products/vendors/1')

    def test_known_product_vendors(self):
        response = self.client.get(
            reverse('product-vendor', kwargs={'id': '1'})).content
        parsed_answer = json.loads(response)
        expected_answer = json.loads(self.expected_products)

        parsed_answer['products'] = sorted(
            parsed_answer['products'], key=lambda k: k['id'])
        expected_answer['products'] = sorted(
            expected_answer['products'], key=lambda k: k['id'])

        self.assertEqual(parsed_answer, expected_answer)
