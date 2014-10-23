from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Vendor
from django.contrib.auth.models import User, Group


class ListVendorTestCase(TestCase):
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
        url = reverse('new-vendor')
        self.assertEqual(url, '/entry/vendors/new')

    def test_list_items(self):
        """
        Tests to see if the list of vendors contains the proper vendors and
        proper vendor data
        """
        response = self.client.get(reverse('list-vendors-edit'))
        items = response.context['item_list']

        vendor_dict = {}

        for vendor in items:
            vendor_id = vendor['link'].split('/')[-1]
            vendor_dict[str(vendor_id)] = vendor

        for vendor in Vendor.objects.all():
            self.assertEqual(
                vendor_dict[str(vendor.id)]['description'], vendor.description)
            self.assertEqual(
                vendor_dict[str(vendor.id)]['name'], vendor.name)
            self.assertEqual(
                vendor_dict[str(vendor.id)]['link'],
                reverse('edit-vendor', kwargs={'id': vendor.id}))
            self.assertEqual(
                vendor_dict[str(vendor.id)]['modified'],
                vendor.modified.strftime("%I:%M %P, %d %b %Y"))
