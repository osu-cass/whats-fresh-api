from django.test import TestCase

from whats_fresh.whats_fresh_api.models import (ProductPreparation, Product,
                                                Preparation)
from django.contrib.gis.db import models


class ProductPreparationTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'product': models.ForeignKey,
            'product_id': models.ForeignKey,
            'preparation': models.ForeignKey,
            'preparation_id': models.ForeignKey,
            'vendorproduct': models.related.RelatedObject,
            'vendors': models.related.RelatedObject,
            'id': models.AutoField
        }

    def test_fields_exist(self):
        model = models.get_model('whats_fresh_api', 'ProductPreparation')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = ProductPreparation._meta.get_all_field_names()
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test___unicode___method(self):
        try:
            ProductPreparation.__unicode__(
                ProductPreparation(
                    product=Product(name='test'),
                    preparation=Preparation(name='test')
                ))
        except AttributeError:
            self.fail("No __unicode__ method found")
