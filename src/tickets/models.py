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


class TicketManager(models.Manager):
    """
    model manager for activity feed,
    return queryset's for the user's and other user's ticket creation actions
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


class Ticket(models.Model):
    """
    a ticket can be either a bug or a feature, a ticket is associated to its creator via a foreign key.
    a ticket can have many people that have voted for it. the tickets url will be its id and its title.
    a ticket must keep track of how many votes and money has been obtained.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, editable=False, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=False, null=True)
    avatar = models.CharField(max_length=100, blank=True, null=True, default='/static/img/avatars/tim.png')
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, blank=False, null=True)
    description = models.CharField(max_length=1000, blank=False, null=True)
    status = models.CharField(max_length=100, default='need help', choices=STATUS_CHOICES)
    votes = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    earned = models.IntegerField(default=0, null=True, blank=True)
    issue = models.CharField(max_length=100, blank=False, null=True, choices=ISSUE_CHOICES)
    slug = models.SlugField(null=True, blank=True)
    vote_profiles = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='vote_profiles_many')
    objects = TicketManager()

    def save(self, *args, **kwargs):
        """
        override save function, on save:
        slug field becomes a slugified version of the tickets title
        username is current users username and avatar assigned for easy access to it
        """
        self.slug = slugify(self.title)
        self.avatar = self.user.profile.avatar
        self.username = self.user.username
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return smart_text(f'{self.issue}: No: {self.id} by {self.username} | {self.title}')

    def get_absolute_url(self):
        """
            depending on if a bug or feature is saved, the user will be returned to the
            bug or feature main page after submitting their ticket
        """
        return reverse(f'tickets:{self.issue}s')


