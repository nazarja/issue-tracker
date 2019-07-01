from django.db import models
from django.conf import settings
from tickets.models import Ticket


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, blank=False, null=True)
    updated_on = models.DateTimeField(auto_now=True)



