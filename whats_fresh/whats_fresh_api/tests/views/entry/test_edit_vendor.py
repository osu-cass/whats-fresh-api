from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Vendor, Story
from django.contrib.auth.models import User, Group


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

    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        user.save()

        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)

        response = self.client.login(
            username='temporary', password='temporary')
        self.assertEqual(response, True)

    def test_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse('edit-vendor', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/vendors/1')

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
            'street': '750 NW Lighthouse Dr', 'story': 1,
            'status': '', 'state': 'OR', 'preparation_ids': '1,2',
            'phone': '', 'name': 'Test Name',
            'latitude': '44.6752643', 'longitude': '-124.072162',
            'location_description': 'Optional Description',
            'email': '', 'description': 'Test Description',
            'contact_name': 'Test Contact', 'city': 'Newport'}

        self.client.post(
            reverse('edit-vendor', kwargs={'id': '1'}), new_vendor)

        # These values are changed by the server after being received from
        # the client/web page. The preparation IDs are going to be changed
        # into vendor_product objects, so we'll not need the preparations_id
        # field
        del new_vendor['preparation_ids']
        del new_vendor['latitude']
        del new_vendor['longitude']
        new_vendor['status'] = None
        new_vendor['phone'] = None
        new_vendor['story'] = Story.objects.get(id=new_vendor['story'])

        vend = Vendor.objects.get(id=1)
        for field in new_vendor:
            self.assertEqual(getattr(vend, field), new_vendor[field])

        self.assertEqual(vend.location.y, 44.6752643)  # latitude
        self.assertEqual(vend.location.x, -124.072162)  # longitude

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
            "location_description": "Location description",
            "contact_name": "A. Persson",
            "story": 1,
            "website": "http://example.com",
            "email": "a@perr.com"
        }

        phone = 5417377627

        form = response.context['vendor_form']
        self.assertEqual(phone, form['phone'].value().national_number)

        for field in fields:
            self.assertEqual(fields[field], form[field].value())

    def test_delete_vendor(self):
        """
        Tests that DELETing entry/vendors/<id> deletes the item
        """
        response = self.client.delete(
            reverse('edit-vendor', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Vendor.DoesNotExist):
            Vendor.objects.get(id=2)

        response = self.client.delete(
            reverse('edit-vendor', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 404)
