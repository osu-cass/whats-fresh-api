from django.test import TestCase

from whats_fresh.whats_fresh_api.models import Theme
from django.contrib.gis.db import models


class ThemeTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'name': models.CharField,
            'background_color': models.TextField,
            'foreground_color': models.TextField,
            'logo': models.ImageField,
            'slogan': models.CharField,
            'site_title': models.CharField,
            'vendors': models.CharField,
            'products': models.CharField,
            'preparations': models.CharField,
            'stories': models.CharField,
            'images': models.CharField,
            'videos': models.CharField,
            'vendors_slug': models.SlugField,
            'products_slug': models.SlugField,
            'preparations_slug': models.SlugField,
            'stories_slug': models.SlugField,
            'images_slug': models.SlugField,
            'videos_slug': models.SlugField,
            'active': models.SlugField,
            'id': models.AutoField
        }

        self.optional_fields = {
            'logo',
            'slogan'
        }

        self.null_fields = {'logo', 'slogan'}

    def test_fields_exist(self):
        model = models.get_model('whats_fresh_api', 'Theme')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = Theme._meta.get_all_field_names()
        self.assertTrue(sorted(fields) == sorted(self.expected_fields.keys()))

    def test___unicode___method(self):
        try:
            Theme.__unicode__(Theme())
        except AttributeError:
            self.fail("No __unicode__ method found")

    def test_optional_fields(self):
        models.get_model('whats_fresh_api', 'Theme')
        for field in self.optional_fields:
            self.assertEqual(
                Theme._meta.get_field_by_name(field)[0].blank, True)
        for field in self.null_fields:
            self.assertEqual(
                Theme._meta.get_field_by_name(field)[0].null, True)
