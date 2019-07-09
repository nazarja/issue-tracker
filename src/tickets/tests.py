from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Ticket
from .forms import TicketForm


class TestTicketsViews(TestCase):
    """
    test tickets views
    """
    def setUp(self):
        username = 'testuser'
        password = 'testpass'

        User = get_user_model()
        user = User.objects.create_user(username, password=password)

        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)
        self.obj = Ticket.objects.create(issue='bug', user=user, title='title')

    def test_bugs_get(self):
        response = self.client.get('/tickets/bugs/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket-list-view.html')

    def test_features_get(self):
        response = self.client.get('/tickets/features/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket-list-view.html')

    def test_ticket_details_get(self):
        response = self.client.get(f'/tickets/{self.obj.id}/{self.obj.slug}/details/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket-detail-view.html')

    def test_ticket_create_post(self):
        response = self.client.post(f'/tickets/bug/create/', {
            'title': 'new title',
            'description': 'a new description posted',
            'status': 'need help'
        })

        obj = Ticket.objects.get(title='new title')
        self.assertEqual(obj.description, 'a new description posted')

    def test_ticket_update_post(self):
        response = self.client.post(f'/tickets/{self.obj.id}/{self.obj.slug}/update/', {
            'title': 'updated new title',
            'description': 'updated new description posted',
            'status': 'in progress'
        })

        obj = Ticket.objects.get(id=self.obj.id)
        self.assertEqual(obj.title, 'updated new title')

    def test_ticket_delete(self):
        response = self.client.delete(f'/tickets/api/{self.obj.id}/delete/')
        self.assertEquals(response.status_code, 204)


class TestTicketForms(TestCase):
    """
    test tickets forms
    """
    def test_form_valid(self):
        title = "the form title"
        description = 'the form description'
        status = 'in progress'

        user = User(id=1)
        user.save()
        obj = Ticket.objects.create(title=title, description=description, status=status, issue='bug', user=user)

        data = {'title': obj.title, 'description': obj.description, 'status': obj.status}
        form = TicketForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('title'), obj.title)
        self.assertNotEqual(form.cleaned_data.get('description'), 'a different description')

    def test_form_invalid(self):
        title = "the form title"
        description = 'the form description'
        status = 'in progress'

        user = User(id=1)
        user.save()

        obj = Ticket.objects.create(title=title, description=description, status=status, issue='bug', user=user)
        data = {'title': obj.title, 'description': '', 'status': obj.status}
        form = TicketForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)


class TestTicketModel(TestCase):
    """
    test ticket models
    """
    def setUp(self):
        user = User(id=1)
        user.save()

        title = 'a test case title'
        Ticket.objects.create(issue="bug", title=title, user=user)

    def test_ticket_slug_created(self):
        obj = Ticket.objects.get(title='a test case title')
        self.assertEqual(obj.slug, 'a-test-case-title')

    def test_ticket_avatar_created(self):
        obj = Ticket.objects.get(title='a test case title')
        self.assertTrue(obj.avatar != '')

    def test_ticket_default_status(self):
        obj = Ticket.objects.get(title='a test case title')
        self.assertTrue(obj.status == 'need help')

    def test_default_integers(self):
        obj = Ticket.objects.get(title='a test case title')
        self.assertEqual(obj.votes, 0)
        self.assertEqual(obj.earned, 0)

    def test_not_empty(self):
        obj = Ticket.objects.get(title='a test case title')
        self.assertTrue(obj.title != '')
        self.assertTrue(obj.description != '')
        self.assertTrue(obj.status in ['need help', 'in progress', 'resolved'])


class TestTicketModelIncreaseVotes(TestCase):
    """
    test ticket models
    """
    def setUp(self):
        user = User(id=1)
        user.save()

        title = 'revenue increase'
        t = Ticket.objects.create(issue="feature", title=title, user=user)
        t.votes += 1
        t.earned += 5
        t.save()

    def test_revenue_increases(self):
        obj = Ticket.objects.get(title='revenue increase')
        self.assertEqual(obj.votes, 1)
        self.assertEqual(obj.earned, 5)



