from django.test import TestCase

from whats_fresh.whats_fresh_api.models import Image
from django.contrib.gis.db import models


class ImageTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'image': models.ImageField,
            'name': models.TextField,
            'caption': models.TextField,
            'product': models.related.RelatedObject,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'product': models.related.RelatedObject,
            'story': models.related.RelatedObject,
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
            image = Image(name="test", image="image.jpg", caption="caption")
            image.save()
            self.assertEqual("test", image.__unicode__())
        except AttributeError:
            self.fail("No __unicode__ method found")

    def test_filename_method(self):
        try:
            Image.filename(Image(image="cat.jpg"))
        except AttributeError:
            self.fail("No __unicode__ method found")

    def test_optional_fields(self):
        models.get_model('whats_fresh_api', 'Image')
        for field in self.optional_fields:
            self.assertEqual(
                Image._meta.get_field_by_name(field)[0].blank, True)
