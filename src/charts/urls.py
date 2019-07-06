from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

app_name = 'charts'

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='charts/charts.html')), name='charts'),
    path('api/data/', include('charts.api.urls'),  name='charts.api.urls'),
]
