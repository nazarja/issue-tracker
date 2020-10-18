from django.db import models
from django.conf import settings
from tickets.models import Ticket
from django.utils import timezone
from django.utils.encoding import smart_text


class CommentManager(models.Manager):
    """
    model manager for activity feed,
    return queryset's for the user's and other user's comments
    """
    def get_latest(self, query=None):
        """
        exclude the user from one queryset,
        include in a separate query to ensure we get current user results
        """
        all_queryset = self.get_queryset().exclude(user=query).order_by('-updated_on')[:5]
        user_queryset = self.get_queryset().filter(user=query).order_by('-updated_on')[:5][:5]

        # join together with a pipe to return as a single queryset
        return all_queryset | user_queryset


class Comment(models.Model):
    """
    comment model uses two foreign keys, a user and the ticket being commented on
    we can now call all comments for a ticket by a particular user, and all tickets with comments
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.DO_NOTHING)
    username = models.CharField(max_length=100, blank=False, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, blank=False, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    objects = CommentManager()

    def __str__(self):
        issue = self.ticket.issue
        username = self.user.username
        return smart_text(f'Comment: #{self.id} on a {issue} by: {username}')

    def save(self, *args, **kwargs):
        # on save assign the current username to the comment username field
        # will be used in html div
        self.username = self.user.username
        super(Comment, self).save(*args, **kwargs)





