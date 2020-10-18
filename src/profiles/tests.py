from django.test import TestCase
from django.contrib.auth import get_user_model


class TestProfileViews(TestCase):
    """
    test profile views
    """
    def setUp(self):
        username = 'testuser'
        password = 'testpass'

        User = get_user_model()
        self.user = User.objects.create_user(username, password=password)

        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_avatar_gallery_get(self):
        self.response = self.client.get('/profiles/change-avatar/')
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'profiles/change_avatar.html')

    def test_change_avatar(self):
        self.response = self.client.post('/profiles/change-avatar/', {
            'url': '/static/img/avatars/helen.jpg'
        })

        self.assertContains(self.response, 'Successfully Changed Avatar')
