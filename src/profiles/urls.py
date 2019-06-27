from django.urls import path
from .views import ChangeAvatarView

app_name = 'profiles'

urlpatterns = [
    path('change_avatar/', ChangeAvatarView.as_view(), name='change_avatar'),
]
