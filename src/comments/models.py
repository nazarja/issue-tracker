from django.db import models
from django.conf import settings
from tickets.models import Ticket
from django.utils.encoding import smart_text


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.DO_NOTHING)
    username = models.CharField(max_length=100, blank=False, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, blank=False, null=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        issue = self.ticket.issue
        username = self.user.username
        return smart_text(f'comment {self.id} on {issue} by {username}')

    def save(self, *args, **kwargs):
        self.username = self.user.username
        super(Comment, self).save(*args, **kwargs)





