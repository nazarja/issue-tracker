from django.urls import path
from django.views.generic import TemplateView

app_name = 'activity_feed'

urlpatterns = [
    path('', TemplateView.as_view(template_name='activity_feed/feed.html'), name='activity_feed'),
]
