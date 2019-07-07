import os
from random import choice
from django.db import models
from django.conf import settings
from allauth.account.signals import user_signed_up, user_logged_in, password_changed
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib import messages
from tickets.models import Ticket
from django.utils import timezone


def get_avatars_files():
    """
    helper function to get the full file path to the avatar image
    """
    path = settings.BASE_DIR + '/static/img/avatars/'
    return os.listdir(path)


def get_random_avatar_picture():
    """
    helper function to assign a random avatar on account sign-up
    """
    return '/static/img/avatars/' + choice(get_avatars_files())


class ProfileManager(models.Manager):
    """
    model manager for activity feed,
    return queryset's for the user's and other user's joining action
    """
    def get_latest(self, query=None):
        """
        exclude the user from one queryset,
        include in a separate query to ensure we get current user results
        """
        all_queryset = self.get_queryset().exclude(user=query).order_by('-created_on')[:5]
        user_queryset = self.get_queryset().filter(user=query)[:1]

        # join together with a pipe to return as a single queryset
        return all_queryset | user_queryset


class Profile(models.Model):
    """
    as django all-auth manages users accounts a separate user profile was required to hook into
    the user model and make custom queries and assignments.
    a onetoone field is used to relate a user to their profile
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=1, related_name='profile', on_delete=models.CASCADE)
    avatar = models.CharField(max_length=260, default=get_random_avatar_picture())
    created_on = models.DateTimeField(default=timezone.now)
    objects = ProfileManager()

    def __str__(self):
        return self.user.username


"""
signals are used below to listen for important events such as pre and post save
"""


@receiver(user_logged_in)
def post_user_logged_in(sender, request, user, **kwargs):
    """
    after user logs in, set the profile session data
    """
    profile = Profile.objects.filter(user_id=user.id).first()
    request.session['avatar'] = profile.avatar


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    admin - create profile at same time as user
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    """
    admin - delete user at same time as profile
    """
    if instance:
        instance.user.delete()


@receiver(password_changed)
def post_password_change(sender, request, user, **kwargs):
    """
    send message on password change for modal popup
    """
    messages.success(request, 'Your password has successfully been changed!')