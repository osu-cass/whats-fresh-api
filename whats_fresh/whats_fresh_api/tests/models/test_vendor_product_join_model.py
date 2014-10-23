from django.test import TestCase

from whats_fresh.whats_fresh_api.models import (VendorProduct,
                                                ProductPreparation, Product,
                                                Preparation, Vendor)
from django.contrib.gis.db import models


class VendorProductJoinTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'vendor': models.ForeignKey,
            'vendor_id': models.ForeignKey,
            'product_preparation': models.ForeignKey,
            'product_preparation_id': models.ForeignKey,
            'vendor_price': models.TextField,
            'available': models.NullBooleanField,
            'id': models.AutoField
        }

        self.optional_fields = {
            'vendor_price',
            'available'
        }

    def test_fields_exist(self):
        model = models.get_model('whats_fresh_api', 'VendorProduct')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = VendorProduct._meta.get_all_field_names()
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test___unicode___method(self):
        try:
            VendorProduct.__unicode__(
                VendorProduct(
                    vendor=Vendor(name='test'),
                    product_preparation=ProductPreparation(
                        product=Product(name='test'),
                        preparation=Preparation(name='test')
                    )
                ))
        except AttributeError:
            self.fail("No __unicode__ method found")

    def test_optional_fields(self):
        models.get_model('whats_fresh_api', 'VendorProduct')
        for field in self.optional_fields:
            self.assertEqual(
                VendorProduct._meta.get_field_by_name(field)[0].blank, True)
