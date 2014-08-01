from django.test import TestCase
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from whats_fresh.models import *
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
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            u'id': models.AutoField
        }
        # Set MEDIA ROOT to sample data for this test
        TEST_ROOT = os.path.abspath(os.path.dirname(__file__))

        self._old_MEDIA_ROOT = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = os.path.join(TEST_ROOT, 'testdata/media/')

        self.image = Image(image='cat.jpg', caption='Meow!')

        # Set creation time variable to test if image.creation records properly
        self.creation_time = datetime.datetime.now()
        self.image.save()

    def test_fields_exist(self):
        model = models.get_model('whats_fresh', 'Image')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = Image._meta.get_all_field_names()
        self.assertTrue(sorted(fields) == sorted(self.expected_fields.keys()))

    def tearDown(self):
        # reset MEDIA_ROOT
        settings.MEDIA_ROOT = self._old_MEDIA_ROOT

    def test_image_uploaded(self):
        """
        Tests that the image was successfully uploaded
        """
        self.assertEquals(self.image.image.url, '/media/cat.jpg')
        self.assertEquals(self.image.caption, 'Meow!')

        self.assertTrue(
            self.image.created.replace(tzinfo=None) - self.creation_time <
            datetime.timedelta(milliseconds=10))

    def test_replace_image(self):
        """
        Tests that the image was properly replaced with a new image.
        Also sets modified time variable for later testing to make
        sure the time variables were properly set and saved.
        """
        # Sleep 25 milliseconds so that the modified time won't be within
        # The defined range of 10 milliseconds
        time.sleep(0.025)

        self.image.image = 'dog.jpg'
        self.mod_time = datetime.datetime.now()
        self.image.save()

        self.assertEquals(self.image.image.url, '/media/dog.jpg')

        self.assertTrue(
            self.image.modified.replace(tzinfo=None) - self.mod_time <
            datetime.timedelta(milliseconds=10))
