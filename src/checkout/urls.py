from django.urls import path
from .views import CheckoutView, CheckoutChargeView, CheckoutSuccessView
from django.contrib.auth.decorators import login_required

app_name = 'checkout'

urlpatterns = [
    path('', login_required(CheckoutView.as_view()), name='checkout-view'),
    path('charge/', login_required(CheckoutChargeView.as_view()), name='checkout-charge-view'),
    path('payment-accepted/', login_required(CheckoutSuccessView.as_view()), name='checkout-success-view'),
]
