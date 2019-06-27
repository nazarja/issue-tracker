from django.db import models
from django.conf import settings
from django.utils import timezone


class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, default='admin')
    email = models.EmailField(max_length=100, null=True)
    subject = models.CharField(max_length=100, blank=False)
    message = models.CharField(max_length=2000, blank=False)
    sent_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name} - {self.subject}'
