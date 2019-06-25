from django.urls import path
from django.views.generic import TemplateView

app_name = 'charts'

urlpatterns = [
    path('', TemplateView.as_view(template_name='charts/charts.html'), name='charts'),
]
