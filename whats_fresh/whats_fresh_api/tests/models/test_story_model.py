from django.test import TestCase

from whats_fresh.whats_fresh_api.models import Story
from django.contrib.gis.db import models


class StoryTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'name': models.TextField,
            'history': models.TextField,
            'facts': models.TextField,
            'buying': models.TextField,
            'preparing': models.TextField,
            'products': models.TextField,
            'season': models.TextField,
            'images': models.ManyToManyField,
            'videos': models.ManyToManyField,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'product': models.related.RelatedObject,
            'vendor': models.related.RelatedObject,
            'id': models.AutoField
        }

    def test_fields_exist(self):
        model = models.get_model('whats_fresh_api', 'Story')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = Story._meta.get_all_field_names()
        self.assertTrue(sorted(fields) == sorted(self.expected_fields.keys()))

    def test_created_modified_fields(self):
        self.assertTrue(Story._meta.get_field('modified').auto_now)
        self.assertTrue(Story._meta.get_field('created').auto_now_add)

    def test___unicode___method(self):
        try:
            story = Story(name="test")
            story.save()
            self.assertEqual("test", story.__unicode__())
        except AttributeError as e:
            raise e
            self.fail("No __unicode__ method found")
