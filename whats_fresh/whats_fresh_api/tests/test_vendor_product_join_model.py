from django.test import TestCase
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from whats_fresh_api.models import *
from django.contrib.gis.db import models


class VendorProductJoinTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'vendor': models.ForeignKey,
            'product': models.ForeignKey,
            'preparation': models.ForeignKey,
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
        self.assertTrue(sorted(fields) == sorted(self.expected_fields.keys()))

    def test___unicode___method(self):
        try:
            result = VendorProduct.__unicode__(VendorProduct())
        except AttributeError as e:
            self.fail("No __unicode__ method found")

    def test_optional_fields(self):
        model = models.get_model('whats_fresh_api', 'VendorProduct')
        for field in self.optional_fields:
            self.assertEqual(VendorProduct._meta.get_field_by_name(field)[0].null, True)
            self.assertEqual(VendorProduct._meta.get_field_by_name(field)[0].blank, True)
