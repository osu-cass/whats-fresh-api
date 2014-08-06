from django.test import TestCase
from django.core.urlresolvers import reverse
"""
class UrlTestCase(TestCase):
    def test_products_endpoints(self):
        " ""
        Tests that /products/, /products/<id>, and /products/describe/
        are valid URLs (with and without the slashes) and resolve the correct
        views.
        " ""
        url = reverse('products')
        assertEqual(url, '/products')

        url = reverse('products', args=[123])
        assertEqual(url, '/products/123')
"""
