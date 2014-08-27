from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh_api.models import *
from django.contrib.gis.db import models
import json


class EditVendorTestCase(TestCase):
    """
    Test that the Edit Vendor page works as expected.

    Things tested:
        URLs reverse correctly
        The outputted page has the correct form fields
        POSTing "correct" data will result in the update of the vendor
            object with the specified ID
        POSTing data with all fields missing (hitting "save" without entering
            data) returns the same field with notations of missing fields
    """
    fixtures = ['test_fixtures']

    def test_url_endpoint(self):
        url = reverse('edit-vendor', kwargs={'id': '1'})
        self.assertEqual(url, '/entry/vendors/1')

    def test_successful_vendor_update(self):
        """
        POST a proper "new vendor" command to the server, and see if the
        new vendor appears in the database
        """
        # Data that we'll post to the server to get the new vendor created
        new_vendor = {
            'zip': '97365', 'website': '', 'hours': '',
            'street': '750 NW Lighthouse Dr', 'story_id': 1,
            'status': '', 'state': 'OR', 'preparation_ids': '1,2',
            'phone': '', 'name': 'Test Name',
            'location_description': 'Optional Description',
            'email': '', 'description': 'Test Description',
            'contact_name': 'Test Contact', 'city': 'Newport'}

        response = self.client.post(
            reverse('edit-vendor', kwargs={'id': '1'}), new_vendor)

        # These values are changed by the server after being received from
        # the client/web page. The preparation IDs are going to be changed
        # into vendor_product objects, so we'll not need the preparations_id
        # field
        del new_vendor['preparation_ids']
        new_vendor['status'] = None
        new_vendor['phone'] = None
        new_vendor['story_id'] = Story.objects.get(id=new_vendor['story_id'])

        vend = Vendor.objects.get(id=1)
        for field in new_vendor:
            self.assertEqual(getattr(vend, field), new_vendor[field])

        # We told it which product preparation ID to use by saving ProdPreps to
        # IDs 1 and 2, and then posting '1,2' as the list of product
        # preparations.
        product_preparations = ([
            vp.product_preparation.id for vp in vend.vendorproduct_set.all()])

        self.assertEqual(sorted(product_preparations), [1, 2])

    def test_form_fields(self):
        """
        Tests to see if the form contains all of the right fields with the
        right initial data
        """
        response = self.client.get(reverse('edit-vendor', kwargs={'id': '1'}))

        fields = {
            "name": "No Optional Null Fields Are Null",
            "status": True,
            "description": "This is a vendor shop.",
            "hours": "Open Tuesday, 10am to 5pm",
            "street": "1633 Sommerville Rd",
            "city": "Sausalito",
            "state": "CA",
            "zip": "94965",
            "location_description": "Location description",
            "contact_name": "A. Persson",
            "story_id": 1,
            "website": "http://example.com",
            "email": "a@perr.com"
        }

        phone = 5417377627

        form = response.context['vendor_form']
        self.assertEqual(phone, form['phone'].value().national_number)

        for field in fields:
            self.assertEqual(fields[field], form[field].value())
