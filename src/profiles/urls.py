from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ChangeAvatarView

app_name = 'profiles'

urlpatterns = [
    path('change-avatar/', login_required(ChangeAvatarView.as_view()), name='change_avatar'),
]
