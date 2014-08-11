from django.test import TestCase
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.core.files import File

from whats_fresh_api.models import *
from django.contrib.gis.db import models

import os
import time
import sys
import datetime


class ImageTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'image': models.ImageField,
            'caption': models.TextField,
            'product': models.related.RelatedObject,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'product': models.related.RelatedObject,
            'id': models.AutoField
        }

        self.optional_fields = {
            'caption'
        }

    def test_fields_exist(self):
        model = models.get_model('whats_fresh_api', 'Image')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_parameters(self):
        self.assertEqual(
            Image._meta.get_field_by_name('image')[0].upload_to,
            'images')

    def test_no_additional_fields(self):
        fields = Image._meta.get_all_field_names()
        self.assertTrue(sorted(fields) == sorted(self.expected_fields.keys()))

    def test_created_modified_fields(self):
        self.assertTrue(Image._meta.get_field('modified').auto_now)
        self.assertTrue(Image._meta.get_field('created').auto_now_add)

    def test___unicode___method(self):
        try:
            result = Image.__unicode__(Image())
        except AttributeError as e:
            self.fail("No __unicode__ method found")

    def test_filename_method(self):
        try:
            result = Image.filename(Image(image="cat.jpg"))
        except AttributeError as e:
            self.fail("No __unicode__ method found")

    def test_optional_fields(self):
        model = models.get_model('whats_fresh_api', 'Image')
        for field in self.optional_fields:
            self.assertEqual(Image._meta.get_field_by_name(field)[0].blank, True)
