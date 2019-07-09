from django.test import TestCase
from django.contrib.auth import get_user_model
from tickets.models import Ticket
from .models import Order


class TestOrderViews(TestCase):
    """
    test chartout views
    """
    def setUp(self):
        username = 'testuser'
        password = 'testpass'

        User = get_user_model()
        user = User.objects.create_user(username, password=password)
        logged_in = self.client.login(username=username, password=password)

        self.assertTrue(logged_in)

        # add item to cart
        self.response = self.client.get('/cart/')
        self.obj = Ticket.objects.create(issue='bug', user=user, title='I am the cart object title')
        self.client.post('/cart/create/', {
            'id': self.obj.id,
            'value': 5,
            'votes': 1,
        })

    def test_checkout_view_does_not_redirect(self):
        self.response = self.client.get('/checkout/')
        self.assertTrue(self.response.status_code, 200)

    def test_success_view(self):
        self.response = self.client.get('/checkout/payment-accepted/')
        self.assertContains(self.response, 'Your Payment Has Been Accepted')


class TestOrderModel(TestCase):
    """
    test order model
    """
    def setUp(self):
        username = 'testuser'
        password = 'testpass'

        User = get_user_model()
        self.user = User.objects.create_user(username, password=password)

        title = 'a test case title'
        self.ticket = Ticket.objects.create(issue="bug", title=title, user=self.user)

        order = Order.objects.create(user=self.user, votes=20, total=5)
        order.ticket.add(self.ticket)

    def test_order_created(self):
        obj = Order.objects.get(votes=20)
        self.assertEqual(obj.votes, 20)

    def test_ticket_added_to_order(self):
        obj = Order.objects.get(votes=20)
        self.assertTrue(self.ticket in obj.ticket.all())

    def test_correct_user_added_to_order(self):
        obj = Order.objects.get(votes=20)
        self.assertTrue(self.user == obj.user)

