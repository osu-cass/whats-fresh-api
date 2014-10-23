from django.test import TestCase
from django.core.urlresolvers import reverse
from whats_fresh.whats_fresh_api.models import Product
from django.contrib.auth.models import User, Group


class ListProductTestCase(TestCase):
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
            reverse('edit-product', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/products/1')

    def test_url_endpoint(self):
        url = reverse('entry-list-products')
        self.assertEqual(url, '/entry/products')

    def test_list_items(self):
        """
        Tests to see if the list of products contains the proper products and
        proper product data
        """
        response = self.client.get(reverse('entry-list-products'))
        items = response.context['item_list']

        product_dict = {}

        for product in items:
            product_id = product['link'].split('/')[-1]
            product_dict[str(product_id)] = product

        for db_product in Product.objects.all():
            list_product = product_dict[str(db_product.id)]
            self.assertEqual(
                list_product['description'],
                db_product.description)
            self.assertEqual(
                list_product['name'], db_product.name)
            self.assertEqual(
                list_product['link'],
                reverse('edit-product', kwargs={'id': db_product.id}))
            self.assertEqual(
                list_product['modified'],
                db_product.modified.strftime("%I:%M %P, %d %b %Y"))
