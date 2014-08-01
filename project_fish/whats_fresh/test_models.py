from django.test import TestCase
from django.conf import settings

from whats_fresh.models import *
from django.contrib.gis.db import models

import os
import time
import sys
import datetime

class ImageTestCase(TestCase):
    def setUp(self):
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
        self.assertEqual(
            models.ImageField,
            type(model._meta.get_field_by_name('image')[0]))
        self.assertEqual(
            models.TextField,
            type(model._meta.get_field_by_name('caption')[0]))
        self.assertEqual(
            models.DateTimeField,
            type(model._meta.get_field_by_name('created')[0]))
        self.assertEqual(
            models.DateTimeField,
            type(model._meta.get_field_by_name('modified')[0]))

    def test_no_additional_fields(self):
        fields = Image._meta.get_all_field_names()
        expected_fields = ['image', 'caption', 'created', 'modified', u'id']

        self.assertTrue(sorted(fields) == sorted(expected_fields))



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
            datetime.timedelta(milliseconds = 10))

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
            datetime.timedelta(milliseconds = 10))


class VendorTestCase(TestCase):
    def test_fields_exist(self):
        model = models.get_model('whats_fresh', 'Vendor')
        self.assertEqual(
            models.TextField,
            type(model._meta.get_field_by_name('name')[0]))
        self.assertEqual(
            models.TextField,
            type(model._meta.get_field_by_name('description')[0]))
        self.assertEqual(
            models.TextField,
            type(model._meta.get_field_by_name('street')[0]))
        self.assertEqual(
            models.TextField,
            type(model._meta.get_field_by_name('city')[0]))
        self.assertEqual(
            models.TextField,
            type(model._meta.get_field_by_name('state')[0]))
        self.assertEqual(
            models.TextField,
            type(model._meta.get_field_by_name('zip')[0]))
        self.assertEqual(
            models.TextField,
            type(model._meta.get_field_by_name('location_description')[0]))
        self.assertEqual(
            models.TextField,
            type(model._meta.get_field_by_name('contact_name')[0]))
        self.assertEqual(
            models.FloatField,
            type(model._meta.get_field_by_name('lat')[0]))
        self.assertEqual(
            models.FloatField,
            type(model._meta.get_field_by_name('long')[0]))
        self.assertEqual(
            models.URLField,
            type(model._meta.get_field_by_name('website')[0]))
        self.assertEqual(
            models.EmailField,
            type(model._meta.get_field_by_name('email')[0]))
        self.assertEqual(
            PhoneNumberField,
            type(model._meta.get_field_by_name('phone')[0]))

    def no_additional_fields(self):
        fields = Vendor._meta.get_all_field_names()
        expected_fields = ['name', 'description', 'street', 'city', 'state',
                           'zip', 'location_description', 'contact_name',
                           'lat', 'long', 'website', 'email', 'phone', u'id']

        self.assertTrue(sorted(fields) == sorted(expected_fields))

