from django.test import TestCase


class TestPagesViews(TestCase):
    """
    test pages
    """
    def setUp(self):
        self.client = Client()

    def test_index_get(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/index.html')

    def test_faq_get(self):
        response = self.client.get('/faq/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/faq.html')