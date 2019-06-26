from django.db import models
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver


def get_random_avatar_picture():
    return '/static/img/avatars/molly.png'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=260, default=get_random_avatar_picture())

    def __str__(self):
        return self.user.username


@receiver(user_signed_up)
def after_user_signed_up(sender, request, user, **kwargs):
    Profile.objects.create(user=user)


@receiver(user_signed_up)
def save_extended_user_profile(sender, user, **kwargs):
    user.profile.save()


@receiver(user_logged_in)
def after_user_logged_in(sender, request, user, **kwargs):
    profile = Profile.objects.filter(user_id=user.id).first()
    request.session['avatar'] = profile.avatar
