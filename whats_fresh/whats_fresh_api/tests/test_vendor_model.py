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
            'street': models.TextField,
            'city': models.TextField,
            'state': models.TextField,
            'zip': models.TextField,
            'location_description': models.TextField,
            'contact_name': models.TextField,
            'lat': models.FloatField,
            'long': models.FloatField,
            'website': models.URLField,
            'email': models.EmailField,
            'phone': PhoneNumberField,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'story_id': models.ForeignKey,
            'product': models.ManyToManyField,
            'id': models.AutoField
        }

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
