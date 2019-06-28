from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.utils.encoding import smart_text


STATUS_CHOICES = (
    ('need help', 'need help'),
    ('in progress', 'in progress'),
    ('resolved', 'resolved'),
)


class AbstractTicket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, editable=False, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=200, blank=False, null=True)
    description = models.CharField(max_length=2000, blank=False, null=True)
    status = models.CharField(max_length=100, default='needs votes', choices=STATUS_CHOICES)
    votes = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        abstract = True


class Bug(AbstractTicket):
    vote_cost = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(Bug, self).save(*args, **kwargs)

    def __str__(self):
        return smart_text(self.title)


class Feature(AbstractTicket):
    vote_cost = models.IntegerField(default=5)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(Feature, self).save(*args, **kwargs)

    def __str__(self):
        return smart_text(self.title)

