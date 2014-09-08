from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
from django.contrib.auth.models import User
import json


class EditProductTestCase(TestCase):
    """
    Test that the Edit Product page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the update of the product
            object with the specified ID
        POSTing data with all fields missing (hitting "save" without entering
            data) returns the same field with notations of missing fields
    """
    fixtures = ['test_fixtures']

    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        user.save()

        self.client.post(
            reverse('login'),
            {'username': 'temporary', 'password': 'temporary'})

    def test_url_endpoint(self):
        url = reverse('edit-product', kwargs={'id': '1'})
        self.assertEqual(url, '/entry/products/1')

    def test_successful_product_update(self):
        """
        POST a proper "update product" command to the server, and see if the
        update appears in the database
        """
        # Data that we'll post to the server to get the product updated
        new_product = {'name': 'Salmon', 'variety': 'Pacific', 'story_id': 1,
                  'alt_name': 'Pacific Salmon', 'origin': 'The Pacific',
                  'description': 'It\'s salmon -- from the Pacific!',
                  'season': 'Always', 'available': '', 'image_id': 1,
                  'market_price': '$3 a pack', 'preparation_ids': '1,2',
                  'link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}

        response = self.client.post(
            reverse('edit-product', kwargs={'id': '1'}), new_product)

        # These values are changed by the server after being received from
        # the client/web page.
        new_product['available'] = None
        new_product['story_id'] = Story.objects.get(id=new_product['story_id'])
        new_product['image_id'] = Image.objects.get(id=new_product['image_id'])

        del new_product['preparation_ids']

        product = Product.objects.get(id=1)
        for field in new_product:
            self.assertEqual(getattr(product, field), new_product[field])

        preparations = ([
            preparation.id for preparation in product.preparations.all()])
        self.assertEqual(sorted(preparations), [1, 2])

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(
            reverse('edit-product', kwargs={'id': '1'}))

        fields = {
            "name": "Ezri Dax",
            "variety": "Freshwater Eel",
            "alt_name": "Jadzia",
            "description": "That's not actually an eel, it's a symbiote.",
            "origin": "Trill",
            "season": "Season 7",
            "available": True,
            "market_price": "$32.64 per season",
            "link": "http://www.amazon.com/Star-Trek-Deep-Space-Nine/dp/B00008KA57/",
            "image_id": 2,
            "story_id": 2
        }
        form = response.context['product_form']

        for field in fields:
            self.assertEqual(fields[field], form[field].value())
