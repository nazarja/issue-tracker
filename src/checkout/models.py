from django.db import models
from tickets.models import Ticket
from django.utils import timezone
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderManager(models.Manager):
    def get_latest(self, query=None):
        all_queryset = self.get_queryset().exclude(user=query).order_by('-created_on')[:5]
        user_queryset = self.get_queryset().filter(user=query).order_by('-created_on')[:5]
        return all_queryset | user_queryset


class Order(models.Model):
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
