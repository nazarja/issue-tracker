from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
from .forms import OrderForm, PaymentForm
import stripe

stripe_api_key = settings.STRIPE_SECRET


class CheckoutView(View):
    template_name = 'checkout/checkout.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['form'] = OrderForm()
        self.context['payment_form'] = PaymentForm()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        pass
