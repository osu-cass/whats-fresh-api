from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class NewVendorTestCase(TestCase):
    """
    Test that the New Vendor page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the creation of a new
            object with the specified details
        POSTing data with all fields missing (hitting "save" without entering
            data) returns the same field with notations of missing fields
        POSTing a valid object with a bad address returns an error saying
            bad adddress. This behaviour may be changed in the future.
    """
    def test_url_endpoint(self):
        url = reverse('new-vendor')
        self.assertEqual(url, '/entry/vendors/new')

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields
        """
        response = self.client.get(reverse('new-vendor'))

        fields = {'name': 'input', 'description': 'input', 'hours': 'input',
                  'story_id': 'select', 'status': 'select', 'street': 'input',
                  'city': 'input', 'state': 'input', 'zip': 'input',
                  'location_description': 'textarea', 'contact_name': 'input',
                  'website': 'input', 'email': 'input', 'phone': 'input'}
        form = response.context['vendor_form']

        for field in fields:
            # for the Edit tests, you should be able to access
            # form[field].value
            self.assertIn(fields[field], str(form[field]))

    def test_successful_vendor_creation(self):
        """
        POST a proper "new vendor" command to the server, and see if the
        new vendor appears in the database
        """
        # Create objects that we'll be setting as the foreign objects for
        # our test vendor

        # It needs a story, and we'll want multiple product_preparations to
        # allow us to test the multi-product logic.

        # We can't predict what the ID of the new vendor will be, so we can
        # delete all of the vendors, and then choose the only vendor left
        # after creation.
        Vendor.objects.all().delete()

        Story.objects.create(id=1)
        product = Product.objects.create(id=1)
        preparation = Preparation.objects.create(id=1)

        ProductPreparation.objects.create(
            id=1, product=product, preparation=preparation)
        ProductPreparation.objects.create(
            id=2, product=product, preparation=preparation)

        # Data that we'll post to the server to get the new vendor created
        new_vendor = {
            'zip': '97365', 'website': '', 'hours': 'optional hours',
            'street': '750 NW Lighthouse Dr', 'story_id': 1,
            'status': '', 'state': 'OR', 'preparation_ids': '1,2',
            'phone': '', 'name': 'Test Name',
            'location_description': 'Optional Description',
            'email': '', 'description': 'Test Description',
            'contact_name': 'Test Contact', 'city': 'Newport'}

        response = self.client.post(reverse('new-vendor'), new_vendor)

        # These values are changed by the server after being received from
        # the client/web page. The preparation IDs are going to be changed
        # into vendor_product objects, so we'll not need the preparations_id
        # field
        del new_vendor['preparation_ids']
        new_vendor['status'] = None
        new_vendor['phone'] = None
        new_vendor['story_id'] = Story.objects.get(id=new_vendor['story_id'])

        vend = Vendor.objects.all()[0]
        for field in new_vendor:
            self.assertEqual(getattr(vend, field), new_vendor[field])

        # We told it which product preparation ID to use by saving ProdPreps to
        # IDs 1 and 2, and then posting '1,2' as the list of product
        # preparations.
        product_preparations = ([
            vp.product_preparation.id for vp in vend.vendorproduct_set.all()])

        self.assertEqual(sorted(product_preparations), [1, 2])

    def test_no_data_error(self):
        """
        POST a "new vendor" command to the server missing all of the
        required fields, and test to see what the error comes back as.
        """
        # Create a list of all objects before sending bad POST data
        all_vendors = Vendor.objects.all()

        new_vendor = {
            'zip': '', 'website': '', 'street': '', 'story_id': '',
            'status': '', 'state': '', 'preparation_ids': None,
            'phone': '', 'name': '', 'location_description': '',
            'email': '', 'description': '', 'contact_name': '',
            'city': '', 'hours': ''}

        response = self.client.post(reverse('new-vendor'))

        # Test non-automatically generated errors written into the view
        self.assertIn(
            'You must choose at least one product.',
            response.context['errors'])
        self.assertIn('Full address is required.', response.context['errors'])

        required_fields = [
            'city', 'name', 'zip', 'story_id', 'long', 'lat', 'state',
            'street', 'contact_name', 'description']
        for field_name in required_fields:
            self.assertIn(field_name, response.context['vendor_form'].errors)

        # Test that we didn't add any new objects
        self.assertTrue(list(Vendor.objects.all()) == list(all_vendors))

    def test_bad_address(self):
        """
        POST a "new vendor" to the server with a bad address -- a non-existant
        street -- and test that a Bad Address error is returned.

        This test contains the same POST data as the
        test_successful_vendor_creation, but with a bad address. This means
        the only error returned should be a Bad Address error.
        """
        # Create a list of all objects before sending bad POST data
        all_vendors = Vendor.objects.all()

        # Create objects that we'll be setting as the foreign objects for
        # our test vendor

        # It needs a story, and we'll want multiple product_preparations to
        # allow us to test the multi-product logic.
        Story.objects.create(id=1)
        product = Product.objects.create(id=1)
        preparation = Preparation.objects.create(id=1)

        ProductPreparation.objects.create(
            id=1, product=product, preparation=preparation)
        ProductPreparation.objects.create(
            id=2, product=product, preparation=preparation)

        # Data that we'll post to the server to get the new vendor created
        new_vendor = {
            'zip': '97477', 'website': '', 'hours': '',
            'street': '123 Fake Street', 'story_id': 1,
            'status': '', 'state': 'OR', 'preparation_ids': '1,2',
            'phone': '', 'name': 'Test Name',
            'location_description': 'Optional Description',
            'email': '', 'description': 'Test Description',
            'contact_name': 'Test Contact', 'city': 'Springfield'}

        response = self.client.post(reverse('new-vendor'), new_vendor)

        # Test that the bad address returns a bad address
        self.assertIn('Bad address!', response.context['errors'])

        # Test that we didn't add any new objects
        self.assertTrue(list(Vendor.objects.all()) == list(all_vendors))
