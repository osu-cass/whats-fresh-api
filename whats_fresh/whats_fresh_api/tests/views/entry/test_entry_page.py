from django.test import TestCase
from django.contrib.auth.models import User, Group


class EditVendorTestCase(TestCase):
    """
    Test that the Entry page requires login.
    """
    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        user.save()

        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)

        response = self.client.login(username='temporary', password='temporary')
        self.assertEqual(response, True)

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/login?next=/entry')

    def test_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)