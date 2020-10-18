from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from comments.models import Comment
from tickets.models import Ticket


class TestCommentViews(TestCase):
    """
    test comments views
    """
    def setUp(self):
        username = 'testuser'
        password = 'testpass'

        User = get_user_model()
        user = User.objects.create_user(username, password=password)

        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)

        self.ticket = Ticket.objects.create(user=user, title='test ticket comments')
        self.comment = Comment.objects.create(user=user, ticket=self.ticket, text='I am the comment text')

    def test_comments_get(self):
        comments = Comment.objects.get(ticket=self.ticket)
        self.assertEqual(comments.text, 'I am the comment text')

    def test_comments_create(self):
        self.response = self.client.post(f'/comments/api/{self.ticket.id}/create/', {
            'text': 'I am a created comment',
            'ticket': self.ticket.id,
        })

        comment = Comment.objects.get(text='I am a created comment')
        self.assertTrue(comment.ticket == self.ticket)

    def test_comments_update(self):
        response = self.client.put(f'/comments/api/{self.comment.id}/update/', {
            'id': self.comment.id,
            'text': 'updated new comment post'
        })

        obj = Comment.objects.get(id=self.comment.id)
        self.assertEqual(obj.text, 'updated new title')

    def test_comments_delete(self):
        self.response = self.client.delete('/comments/api/1/delete/')
        self.assertEquals(self.response.status_code, 204)


class TestCommentModel(TestCase):
    """
    test comments model
    """
    def setUp(self):
        self.user = User(id=1)
        self.user.save()

        title = 'a test case title'
        text = 'I am the comment text'

        self.ticket = Ticket.objects.create(issue="bug", title=title, user=self.user)
        self.comment = Comment.objects.create(user=self.user, ticket=self.ticket, text=text)

    def test_ticket_title_is_created(self):
        obj = Comment.objects.get(id=self.comment.id)
        self.assertEqual(obj.text, 'I am the comment text')

    def test_ticket_is_added_to_comment(self):
        obj = Comment.objects.get(id=self.comment.id)
        self.assertTrue(self.comment.ticket == self.ticket)

    def test_ensure_comment_creates_dates(self):
        obj = Comment.objects.get(id=self.comment.id)
        self.assertTrue(obj.created_on)
        self.assertTrue(obj.updated_on)

    def test_comment_has_username(self):
        obj = Comment.objects.get(id=self.comment.id)
        self.assertEqual(obj.username, self.user.username)

