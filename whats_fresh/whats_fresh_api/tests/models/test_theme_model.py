import django.forms as forms
from django.test import TestCase
from whats_fresh.whats_fresh_api.models import Theme
from whats_fresh.whats_fresh_api.forms import ThemeAdminForm
from django.contrib.gis.db import models


class ThemeTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'name': models.CharField,
            'background_color': models.TextField,
            'foreground_color': models.TextField,
            'header_color': models.TextField,
            'font_color': models.TextField,
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
            'active': models.CharField,
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

    def test_overlapping_form_fields(self):

        form = ThemeAdminForm(data={
            'name': 'Test Name',
            'background_color': 'rgb(81, 114, 133)',
            'foreground_color': 'rgb(81, 114, 133)',
            'header_color': 'rgb(255, 255, 255)',
            'font_color': 'rgb(51, 51, 51)',
            'logo': 'cat.jpg',
            'slogan': 'Test Slogan',
            'site_title': 'Test Title',
            'vendors': 'vendors',
            'products': 'products',
            'preparations': 'preparations',
            'stories': 'stories',
            'images': 'images',
            'videos': 'videos',
            'vendors_slug': 'slug',
            'products_slug': 'slug',
            'preparations_slug': 'slug',
            'stories_slug': 'slug',
            'images_slug': 'slug',
            'videos_slug': 'slug',
            'active': 'No'})

        self.assertFalse(form.is_valid())

        with self.assertRaises(forms.ValidationError) as v_err:
            form.clean()
        self.assertIn("Cannot use slug", v_err.exception[0])

    def test_no_overlapping_fields(self):

        form = ThemeAdminForm(data={
            'name': 'Test Name',
            'background_color': 'rgb(81, 114, 133)',
            'foreground_color': 'rgb(81, 114, 133)',
            'header_color': 'rgb(255, 255, 255)',
            'font_color': 'rgb(51, 51, 51)',
            'logo': 'cat.jpg',
            'slogan': 'Test Slogan',
            'site_title': 'Test Title',
            'vendors': 'vendors',
            'products': 'products',
            'preparations': 'preparations',
            'stories': 'stories',
            'images': 'images',
            'videos': 'videos',
            'vendors_slug': 'vendors',
            'products_slug': 'products',
            'preparations_slug': 'preparations',
            'stories_slug': 'stories',
            'images_slug': 'images',
            'videos_slug': 'videos',
            'active': 'No'})

        self.assertTrue(form.is_valid())
