from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import *
from django.contrib.gis.db import models
from django.contrib.auth.models import User, Group, Permission

import json


class NewProductTestCase(TestCase):
    """
    Test that the New Product page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the creation of a new
            object with the specified details
        POSTing data with all fields missing (hitting "save" without entering
            data) returns the same field with notations of missing fields
    """
    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        user.save()

        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)

        response = self.client.login(username='temporary', password='temporary')
        self.assertEqual(response, True)
    
    def test_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse('edit-preparation', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/preparations/1')
        
    def test_url_endpoint(self):
        url = reverse('new-product')
        self.assertEqual(url, '/entry/products/new')

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(reverse('new-product'))

        fields = {'name': 'input', 'variety': 'input', 'story_id': 'select',
                  'alt_name': 'input', 'description': 'input',
                  'origin': 'input', 'season': 'input', 'available': 'select',
                  'market_price': 'input', 'link': 'input',
                  'image_id': 'select'}
        form = response.context['product_form']

        for field in fields:
            # for the Edit tests, you should be able to access
            # form[field].value
            self.assertIn(fields[field], str(form[field]))

    def test_successful_product_creation(self):
        """
        POST a proper "new product" command to the server, and see if the
        new product appears in the database
        """
        # Create objects that we'll be setting as the foreign objects for
        # our test product

        # It needs a story, and we'll want multiple product_preparations to
        # allow us to test the multi-product logic.

        # We can't predict what the ID of the new product will be, so we can
        # delete all of the vendors, and then choose the only vendor left
        # after creation.
        Product.objects.all().delete()

        Story.objects.create(id=1)
        Preparation.objects.create(id=1)
        Preparation.objects.create(id=2)
        Image.objects.create(id=1)

        # Data that we'll post to the server to get the new vendor created
        new_product = {'name': 'Salmon', 'variety': 'Pacific', 'story_id': 1,
                  'alt_name': 'Pacific Salmon', 'origin': 'The Pacific',
                  'description': 'It\'s salmon -- from the Pacific!',
                  'season': 'Always', 'available': '', 'image_id': 1,
                  'market_price': '$3 a pack', 'preparation_ids': '1,2',
                  'link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}

        response = self.client.post(reverse('new-product'), new_product)

        # These values are changed by the server after being received from
        # the client/web page.
        new_product['available'] = None
        new_product['story_id'] = Story.objects.get(id=new_product['story_id'])
        new_product['image_id'] = Image.objects.get(id=new_product['image_id'])

        del new_product['preparation_ids']

        product = Product.objects.all()[0]
        for field in new_product:
            self.assertEqual(getattr(product, field), new_product[field])

        preparations = ([
            preparation.id for preparation in product.preparations.all()])
        self.assertEqual(sorted(preparations), [1, 2])

    def test_no_data_error(self):
        """
        POST a "new product" command to the server missing all of the
        required fields, and test to see what the error comes back as.
        """
        # Create a list of all objects before sending bad POST data
        all_products = Product.objects.all()

        response = self.client.post(reverse('new-product'))
        required_fields = ['name', 'description', 'season', 'market_price']
        for field_name in required_fields:
            self.assertIn(field_name, response.context['product_form'].errors)

        # Test that we didn't add any new objects
        self.assertTrue(list(Product.objects.all()) == list(all_products))
