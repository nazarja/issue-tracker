from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ActivityFeedListView


app_name = 'activity_feed'

urlpatterns = [
    path('', login_required(ActivityFeedListView.as_view()), name='activity_feed'),
]
