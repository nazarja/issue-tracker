from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ContactFormModel(models.Model):
    # user = models.ForeignKey(User, default=0, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    subject = models.CharField(max_length=100, blank=False)
    message = models.CharField(max_length=2000, blank=False)
    sent_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name} - {self.subject}'
