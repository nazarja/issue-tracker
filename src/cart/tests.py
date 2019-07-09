from django.test import TestCase
from django.contrib.auth import get_user_model
from tickets.models import Ticket


class TestCartViews(TestCase):
    """
    test cart views
    """

    def setUp(self):
        username = 'testuser'
        password = 'testpass'

        User = get_user_model()
        user = User.objects.create_user(username, password=password)
        logged_in = self.client.login(username=username, password=password)

        self.assertTrue(logged_in)
        self.response = self.client.get('/cart/')
        self.obj = Ticket.objects.create(issue='bug', user=user, title='I am the cart object title')

    def test_cart_get(self):
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'cart/cart.html')

    def test_cart_is_empty(self):
        self.assertContains(self.response, 'You dont have anything in your cart right now')

    def test_cart_is_not_empty(self):
        self.client.post('/cart/create/', {
            'id': self.obj.id,
            'value': 5,
            'votes': 1,
        })

        self.response = self.client.get('/cart/')
        self.assertContains(self.response, 'I am the cart object title')

    def test_context_processor(self):
        self.client.post('/cart/create/', {
            'id': self.obj.id,
            'value': 5,
            'votes': 1,
        })

        self.response = self.client.get('/cart/')
        self.assertEqual(self.response.context['cart_count'], 1)
        self.assertEqual(self.response.context['cart_total'], 5)
        self.assertEqual(self.response.context['cart_votes'], 1)

    def test_cart_has_been_updated(self):
        self.client.post('/cart/create/', {
            'id': self.obj.id,
            'value': 5,
            'votes': 1,
        })

        self.response = self.client.get('/cart/')
        self.assertEqual(self.response.context['cart_count'], 1)

        self.client.post('/cart/update/', {
            'data': '',
        })

        self.response = self.client.get('/cart/')
        self.assertEqual(len(self.response.context['cart_items']), 0)
