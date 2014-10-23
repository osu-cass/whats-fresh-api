from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User


class LogoutViewTestCase(TestCase):

    """
    Test the logout view:
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
        self.client.login(**self.user_credentials)

        self.assertEqual(self.client.session['_auth_user_id'], self.user.pk)

        self.client.get('/logout')
        self.assertTrue('_auth_user_id' not in self.client.session)
