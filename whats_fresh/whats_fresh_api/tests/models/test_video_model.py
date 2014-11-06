from django.test import TestCase

from whats_fresh.whats_fresh_api.models import Video
from django.contrib.gis.db import models


class VideoTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'video': models.URLField,
            'caption': models.TextField,
            'name': models.TextField,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'story': models.related.RelatedObject,
            'id': models.AutoField
        }

        self.optional_fields = {
            'caption'
        }

    def test_fields_exist(self):
        model = models.get_model('whats_fresh_api', 'Video')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = Video._meta.get_all_field_names()
        self.assertTrue(sorted(fields) == sorted(self.expected_fields.keys()))

    def test_created_modified_fields(self):
        self.assertTrue(Video._meta.get_field('modified').auto_now)
        self.assertTrue(Video._meta.get_field('created').auto_now_add)

    def test_optional_fields(self):
        for field in self.optional_fields:
            self.assertEqual(
                Video._meta.get_field_by_name(field)[0].blank, True)
