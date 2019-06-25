from django.urls import path
from django.views.generic import TemplateView

app_name = 'tickets'

urlpatterns = [
    path('bugs/', TemplateView.as_view(template_name='tickets/bugs.html'), name='bugs'),
    path('features/', TemplateView.as_view(template_name='tickets/features.html'), name='features'),
]
