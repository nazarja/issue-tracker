from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import BugListView, FeatureListView

app_name = 'tickets'

urlpatterns = [
    path('bugs/', login_required(BugListView.as_view()), name='bugs'),
    path('features/', login_required(FeatureListView.as_view()), name='features'),
]
