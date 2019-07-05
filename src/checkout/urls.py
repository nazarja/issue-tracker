from django.urls import path
from .views import CheckoutView
from django.contrib.auth.decorators import login_required

app_name = 'checkout'

urlpatterns = [
    path('', login_required(CheckoutView.as_view()), name='checkout-view'),
]
