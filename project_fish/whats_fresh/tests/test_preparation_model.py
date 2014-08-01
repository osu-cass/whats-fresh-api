from django.test import TestCase
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from whats_fresh.models import *
from django.contrib.gis.db import models

import os
import time
import sys
import datetime


class PreparationsTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'name': models.TextField,
            'description': models.TextField,
            'additional_info': models.TextField,
            u'id': models.AutoField
        }

    def test_fields_exist(self):
        model = models.get_model('whats_fresh', 'Preparation')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = Vendor._meta.get_all_field_names()
        self.assertTrue(sorted(fields) == sorted(self.expected_fields.keys()))
