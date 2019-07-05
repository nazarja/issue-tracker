import os
from random import choice
from django.db import models
from django.conf import settings
from allauth.account.signals import user_signed_up, user_logged_in, password_changed
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib import messages
from tickets.models import Ticket


def get_avatars_files():
    path = settings.BASE_DIR + '/static/img/avatars/'
    return os.listdir(path)


def get_random_avatar_picture():
    return '/static/img/avatars/' + choice(get_avatars_files())


class ProfileManager(models.Manager):
    def get_latest_profiles(self, query=None):
        queryset = self.get_queryset()
        return queryset


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=1, related_name='profile', on_delete=models.CASCADE)
    avatar = models.CharField(max_length=260, default=get_random_avatar_picture())

    def __str__(self):
        return self.user.username

#  after user logs in, set the profile session data
@receiver(user_logged_in)
def post_user_logged_in(sender, request, user, **kwargs):
    profile = Profile.objects.filter(user_id=user.id).first()
    request.session['avatar'] = profile.avatar


#  Admin create profile at same time as user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


#  Admin - delete user at same time as profile
@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance:
        instance.user.delete()


#  send message on password change for modal popup
@receiver(password_changed)
def post_password_change(sender, request, user, **kwargs):
    messages.success(request, 'Your password has successfully been changed!')