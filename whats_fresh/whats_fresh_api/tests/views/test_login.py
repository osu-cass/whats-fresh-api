from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from whats_fresh_api.models import *
from django.contrib.gis.db import models
from django.contrib.auth.models import User

import os
import time
import sys
import datetime
import json


class LoginViewTestCase(TestCase):
    """
    Test the login view:
        1. the url resolves properly
        2. test that a bad login returns an invalid username/password message
        3. test that a good login without a 'next' tag forwards to the
            expected destination
        4. test that a good login with a 'next' tag forwards to the 'next'
            destination
    """
    def setUp(self):
        self.user_credentials = {
            'name': 'dataentry',
            'password': 'password'}
        self.user = User.objects.create_user(
            user_credentials['name'],
            'data@example.com',
            user_credentials['password'])

    def test_url_endpoint(self):
        url = reverse('login')
        self.assertEqual(url, '/login')

    def test_bad_login(self):
        """
        POST a login command to the server with a bad user/bad password and see
        if we get logged in
        """
        bad_password = {
            'name': self.user_credentials['name'],
            'password': 'bad_password'
        }

        response = self.client.post(
            reverse('login'), bad_password, follow=True)

        self.assertContains(
            response, "Invalid username or password", status_code=401)

        bad_username = {
            'name': 'bad_dataentry',
            'password': self.user_credentials['name']
        }

        response = self.client.post(
            reverse('login'), bad_username, follow=True)

        self.assertContains(
            response, "Invalid username or password", status_code=401)

    def test_good_password(self):
        """
        POST a login command to the server with a good user and see if
        we get logged in
        """
        response = self.client.post(
            reverse('login'), self.user_credentials, follow=True)
        self.assertRedirects(response, '/entry')

   def test_redirect(self):
        """
        POST a login command to the server with a good user and a 'next'
        parameter, and see if we get logged in
        """
        post_data = self.user_credentials.copy()
        post_data['next'] = '/entry/vendors/1'

        response = self.client.post(
            reverse('login'), self.user_credentials, follow=True)
        self.assertRedirects(response, '/entry/vendors/1')
