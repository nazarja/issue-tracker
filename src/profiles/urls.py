from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('change_avatar/', views.ChangeAvatarView.as_view(), name='change_avatar'),
]
