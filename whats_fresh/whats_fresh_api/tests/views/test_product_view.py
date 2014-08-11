from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from whats_fresh_api.models import *
from django.contrib.gis.db import models

import os
import time
import sys
import datetime
import json

class ProductViewTestCase(TestCase):
    fixtures = ['whats_fresh_api/tests/testdata/test_fixtures.json']         
    def test_url_endpoint(self):
        url = reverse('products-list')
        self.assertEqual(url, '/products')

    def test_json_equals(self):
        c = Client()
        response = c.get(reverse('products-list')).content
        parsed_answer = json.loads(response)
        expected_answer = json.loads(self.expected_json)
        self.assertTrue(parsed_answer == expected_answer)
