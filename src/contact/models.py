from django.db import models
from django.conf import settings
from django.utils import timezone


class Contact(models.Model):
    """
    contact form model - will be inherited by contact form
    if an anonymous user sends the form, then it was sent be the admin
    otherwise its associated with the logged in user and their details are pre-populated
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, default='admin')
    email = models.EmailField(max_length=100, null=True)
    subject = models.CharField(max_length=100, blank=False)
    message = models.CharField(max_length=2000, blank=False)
    sent_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Contact Form'
        verbose_name_plural = 'Contact Forms'

    def __str__(self):
        return f'{self.name} - {self.subject}'
