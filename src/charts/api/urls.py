from django.urls import path
from .views import ChartsAPIView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(ChartsAPIView.as_view()), name='charts-api-view'),
]
