from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.encoding import smart_text
from django.urls import reverse
from datetime import datetime

STATUS_CHOICES = (
    ('need help', 'need help'),
    ('in progress', 'in progress'),
    ('resolved', 'resolved'),
)

ISSUE_CHOICES = (
    ('bug', 'bug'),
    ('feature', 'feature')
)


class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, editable=False, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=100, blank=True, null=True, default='/static/img/avatars/steve.jpg')
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=200, blank=False, null=True)
    description = models.CharField(max_length=2000, blank=False, null=True)
    status = models.CharField(max_length=100, default='need help', choices=STATUS_CHOICES)
    votes = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    cost = models.IntegerField(default=0, null=True, blank=True)
    earned = models.IntegerField(default=0, null=True, blank=True)
    issue = models.CharField(max_length=100, blank=False, null=True, choices=ISSUE_CHOICES)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.cost = 5 if self.issue == 'feature' else 0
        self.avatar = self.user.profile.avatar
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return smart_text(f'{self.issue}: {self.title}')

    def get_absolute_url(self):
        if self.issue == 'bug':
            return reverse('tickets:bugs')
        else:
            return reverse('tickets:bugs')

    # could return to newly created / edited ticket url instead ???
    # return reverse("tickets:ticket-detail-view", kwargs={'id': self.id, 'slug': self.slug})
