from django.test import TestCase
from django.contrib.auth import get_user_model


class TestActivityFeedViews(TestCase):
    """
    test activity feed views
    """
    def setUp(self):
        username = 'testuser'
        password = 'testpass'

        User = get_user_model()
        user = User.objects.create_user(username, password=password)
        logged_in = self.client.login(username=username, password=password)

        self.assertTrue(logged_in)
        self.response = self.client.get('/activity-feed/')

    def test_activity_feed_get(self):
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'activity_feed/feed.html')

    def test_activity_feed_has_object_list(self):
        self.assertTrue('object_list' in self.response.context)

    def test_activity_feed_has_user_object_list(self):
        for obj in self.response.context['object_list']:
            self.assertTrue(obj.user.username == 'testuser')

    def test_activity_feed_has_objects(self):
        self.assertContains(self.response, ' You Just Joined!')
