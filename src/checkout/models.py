from django.db import models
from tickets.models import Ticket
from django.utils import timezone
from django.conf import settings


class OrderManager(models.Manager):
    """
    model manager for activity feed,
    return queryset's for the user's and other user's purchases
    """
    def get_latest(self, query=None):
        """
        exclude the user from one queryset,
        include in a separate query to ensure we get current user results
        """
        all_queryset = self.get_queryset().exclude(user=query).order_by('-created_on')[:5]
        user_queryset = self.get_queryset().filter(user=query).order_by('-created_on')[:5]

        # join together with a pipe to return as a single queryset
        return all_queryset | user_queryset


class Order(models.Model):
    """
    feature purchase order model
    a single order can have many tickets associated with it but only  one user
    """
    ticket = models.ManyToManyField(Ticket, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=False, blank=True, on_delete=models.DO_NOTHING)
    votes = models.IntegerField(null=True, blank=False)
    total = models.IntegerField(null=True, blank=False)
    date = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(default=timezone.now)
    objects = OrderManager()

    def __str__(self):
        return f'#{self.id} | Amount:{self.total}  | User: {self.user} | Votes: {self.votes}'

    def save(self, *args, **kwargs):
        self.date = timezone.now()
        super(Order, self).save(*args, **kwargs)
