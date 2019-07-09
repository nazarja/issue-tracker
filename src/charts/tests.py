from django.test import TestCase
from tickets.models import Ticket
from django.contrib.auth import get_user_model


class TestChartsViews(TestCase):
    """
    test charts views
    """
    def setUp(self):
        username = 'testuser'
        password = 'testpass'

        User = get_user_model()
        user = User.objects.create_user(username, password=password)
        logged_in = self.client.login(username=username, password=password)

        self.assertTrue(logged_in)
        self.obj = Ticket.objects.create(issue='bug', user=user, title='I am a charts data object')

    def test_charts_get(self):
        response = self.client.get('/charts/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'charts/charts.html')

    def test_charts_data_get(self):
        response = self.client.get('/charts/api/data/')
        self.assertEquals(response.status_code, 200)

    def test_charts_json_response(self):
        response = self.client.get('/charts/api/data/')
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'highestBugs': [{'title': 'bug: #1', 'votes': 0}],
             'highestFeatures': [], 'highestStatus': [{'earned': 0, 'title': 'bug: #1', 'votes': 0}],
             'highestVotes': [0, 0],
             'numOfTickets': [1, 0],
             'ticketStatus': [1, 0, 0]
             }
        )
