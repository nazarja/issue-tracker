from django.views.generic import ListView
from .models import Bug, Feature


class BugListView(ListView):
    model = Bug
    template_name = 'tickets/bugs.html'
    ordering = ['-updated_on']


class FeatureListView(ListView):
    model = Feature
    template_name = 'tickets/features.html'
    ordering = ['-updated_on']
