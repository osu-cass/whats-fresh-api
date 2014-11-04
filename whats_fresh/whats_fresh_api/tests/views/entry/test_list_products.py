from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Product
from django.contrib.auth.models import User, Group


class ListProductTestCase(TestCase):
    fixtures = ['thirtythree']

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
            reverse('edit-product', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/products/1')

    def test_url_endpoint(self):
        url = reverse('entry-list-products')
        self.assertEqual(url, '/entry/products')

    def test_delete_items(self):
        """
        Tests that DELETing a list of products to the list page deletes
        the items.
        """
        to_delete = [3, 4, 10, 11, 23]

        response = self.client.delete(
            reverse('entry-list-products'), {'delete': [3, 4, 10, 11]})
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Product.DoesNotExist):
            for product in to_delete:
                Product.objects.get(id=product)

        # Test one that doesn't work
        response = self.client.delete(
            reverse('entry-list-products'), {'delete': [100]})
        self.assertEqual(response.status_code, 404)

    def test_list_items(self):
        """
        Tests to see if the list of products contains the proper
        products and proper product data
        """

        page_1 = self.client.get(reverse('entry-list-products')).context
        page_2 = self.client.get(
            '{}?page=2'.format(reverse('entry-list-products'))).context
        page_3 = self.client.get(
            '{}?page=3'.format(reverse('entry-list-products'))).context
        page_4 = self.client.get(
            '{}?page=4'.format(reverse('entry-list-products'))).context
        page_nan = self.client.get(
            '{}?page=NaN'.format(reverse('entry-list-products'))).context

        self.assertEqual(
            list(page_1['item_list']),
            list(Product.objects.all()[:15]))

        self.assertEqual(
            list(page_2['item_list']),
            list(Product.objects.all()[15:30]))

        self.assertEqual(
            list(page_3['item_list']),
            list(Product.objects.all()[30:33]))

        # Page 4 should be identical to Page 3, as these fixtures
        # have enough content for three pages (15 items per page, 33 items)

        self.assertEqual(
            list(page_3['item_list']),
            list(page_4['item_list']))

        # Page NaN should be identical to Page 1, as Django paginator returns
        # the first page if the page is not an int

        self.assertEqual(
            list(page_1['item_list']),
            list(page_nan['item_list']))
