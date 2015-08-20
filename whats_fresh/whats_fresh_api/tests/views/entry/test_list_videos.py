from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from whats_fresh.whats_fresh_api.models import Video
from haystack.query import SearchQuerySet


class ListVideoTestCase(TestCase):
    fixtures = ['thirtythree']

    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        user.save()

        admin_group = Group(name='Administration Users')
        admin_group.save()
        user.groups.add(admin_group)

        response = self.client.login(
            username='temporary', password='temporary')
        self.assertEqual(response, True)

    def test_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse('edit-video', kwargs={'id': '1'}))
        self.assertRedirects(response, '/login?next=/entry/videos/1')

    def test_url_endpoint(self):
        url = reverse('entry-list-videos')
        self.assertEqual(url, '/entry/videos')

    def test_list_items(self):
        """
        Tests to see if the list of videos contains the proper
        videos and proper video data
        """

        page_1 = self.client.get(reverse('entry-list-videos')).context
        page_2 = self.client.get(
            '{}?page=2'.format(reverse('entry-list-videos'))).context
        page_3 = self.client.get(
            '{}?page=3'.format(reverse('entry-list-videos'))).context
        page_4 = self.client.get(
            '{}?page=4'.format(reverse('entry-list-videos'))).context
        page_nan = self.client.get(
            '{}?page=NaN'.format(reverse('entry-list-videos'))).context

        self.assertEqual(
            list(page_1['item_list']),
            list(Video.objects.order_by('name')[:15]))

        self.assertEqual(
            list(page_2['item_list']),
            list(Video.objects.order_by('name')[15:30]))

        self.assertEqual(
            list(page_3['item_list']),
            list(Video.objects.order_by('name')[30:33]))

        # Page 4 should be identical to Page 3, as these fixtures
        # have enough content for three pages (15 items per page, 33 items)

        self.assertEqual(
            list(page_3['item_list']),
            list(page_4['item_list']))

        # Page NaN should be identical to Page 1, as Django paginator returns
        # the first page if the page is not an int

        self.assertEqual(
            list(page_1['item_list']),
            list(page_nan['item_list']))

    def test_search_result(self):
        search_result = self.client.get(
            '{}?search=20'.format(reverse('entry-list-videos'))).context

        self.assertEqual(list(search_result['item_list']),
                         list(item.object for item in
                              SearchQuerySet().models(Video)
                              .autocomplete(content='20'))
                         )
