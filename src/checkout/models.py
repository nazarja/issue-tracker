from django.db import models
from tickets.models import Ticket
from django.utils import timezone


class Order(models.Model):
    full_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=False)
    street_address1 = models.CharField(max_length=40, blank=False)
    street_address2 = models.CharField(max_length=40, blank=False)
    county = models.CharField(max_length=40, blank=False)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.date} | {self.id} | {self.full_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, null=False, on_delete=models.CASCADE)
    votes = models.IntegerField(blank=False)
    total = models.IntegerField(blank=False)

    def __str__(self):
        return f'{self.ticket.id} | {self.total}  | {self.votes}'
