from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from whats_fresh.whats_fresh_api.models import *
from django.contrib.gis.db import models
from django.contrib.auth.models import User

import os
import time
import sys
import datetime
import json


class LogoutViewTestCase(TestCase):
    """
    Test the login view:
        1. the url resolves properly
        2. GETting the page logs the user out
    """
    def setUp(self):
        self.user_credentials = {
            'username': 'dataentry',
            'password': 'password'}
        self.user = User.objects.create_user(
            self.user_credentials['username'],
            'data@example.com',
            self.user_credentials['password'])
        self.user.save()

    def test_url_endpoint(self):
        try:
            url = reverse('logout')
            self.assertEqual(url, '/logout')
        except:
            self.fail('logout url could not be reversed.')

    def test_logout(self):
        """
        Log in, log out using the /logout page, and make sure that
        we're logged out by accessing the /login page without it
        redirecting.
        """
        logged_in = self.client.login(**self.user_credentials)
        self.assertTrue(logged_in) # verify we logged in successfully

        response = self.client.get('/login')
        self.assertContains(
            response, "Please log in below...")
