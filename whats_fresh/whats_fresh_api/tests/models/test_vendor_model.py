from django.test import TestCase
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from whats_fresh_api.models import *
from django.contrib.gis.db import models

import os
import time
import sys
import datetime

class VendorTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'name': models.TextField,
            'description': models.TextField,
            'status': models.NullBooleanField,
            'street': models.TextField,
            'city': models.TextField,
            'state': models.TextField,
            'zip': models.TextField,
            'status': models.NullBooleanField,
            'location_description': models.TextField,
            'hours': models.TextField,
            'contact_name': models.TextField,
            'website': models.URLField,
            'email': models.EmailField,
            'phone': PhoneNumberField,
            'lat': models.FloatField,
            'long': models.FloatField,
            'story_id': models.ForeignKey,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'story_id': models.ForeignKey,
            'products_preparations': models.ManyToManyField,
            'vendorproduct': models.related.RelatedObject,
            'id': models.AutoField
        }

        self.optional_fields = {
            'location_description',
            'website',
            'hours',
            'email',
            'phone'
        }

        self.null_fields = {'story_id'}

    def test_fields_exist(self):
        model = models.get_model('whats_fresh_api', 'Vendor')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = Vendor._meta.get_all_field_names()
        self.assertTrue(sorted(fields) == sorted(self.expected_fields.keys()))

    def test_created_modified_fields(self):
        self.assertTrue(Vendor._meta.get_field('modified').auto_now)
        self.assertTrue(Vendor._meta.get_field('created').auto_now_add)

    def test___unicode___method(self):
        try:
            result = Vendor.__unicode__(Vendor())
        except AttributeError as e:
            self.fail("No __unicode__ method found")

    def test_optional_fields(self):
        model = models.get_model('whats_fresh_api', 'Vendor')
        for field in self.optional_fields:
            self.assertEqual(Vendor._meta.get_field_by_name(field)[0].blank, True)
        for field in self.null_fields:
            self.assertEqual(Vendor._meta.get_field_by_name(field)[0].null, True)
