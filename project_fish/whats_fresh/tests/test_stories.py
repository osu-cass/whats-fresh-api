from django.test import TestCase
from django.conf import settings

from whats_fresh.models import Story

import os
import time
import sys
import datetime

class StoryTestCase(TestCase):
    def setUp(self):
        # Set MEDIA ROOT to sample data for this test
        TEST_ROOT = os.path.abspath(os.path.dirname(__file__))

        self._old_MEDIA_ROOT = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = os.path.join(TEST_ROOT, 'testdata/media/')

        self.story = Story(story='story0.txt')

        # Set creation time variable to test if story.creation records properly
        self.creation_time = datetime.datetime.now()
        self.story.save()

    def tearDown(self):
        # reset MEDIA_ROOT
        settings.MEDIA_ROOT = self._old_MEDIA_ROOT

    def test_story_uploaded(self):
        """
        Tests that the story was successfully uploaded
        """
        self.assertEquals(self.story.story.url, '/media/story0.txt')

        self.assertTrue(
            self.story.created.replace(tzinfo=None) - self.creation_time < 
            datetime.timedelta(milliseconds = 10))

    def test_replace_story(self):
        """
        Tests that the story was properly replaced with a new story.
        Also sets modified time variable for later testing to make
        sure the time variables were properly set and saved.
        """
        # Sleep 25 milliseconds so that the modified time won't be within
        # The defined range of 10 milliseconds
        time.sleep(0.025)

        self.story.story = 'story1.txt'
        self.mod_time = datetime.datetime.now()
        self.story.save()

        self.assertEquals(self.story.story.url, '/media/story1.txt')

        self.assertTrue(
            self.story.modified.replace(tzinfo=None) - self.mod_time <
            datetime.timedelta(milliseconds = 10))

