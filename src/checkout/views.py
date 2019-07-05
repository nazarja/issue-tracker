from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from django.contrib import messages
from .forms import OrderForm
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(View):
    template_name = 'checkout/checkout.html'
    context = {'publishable': settings.STRIPE_PUBLISHABLE_KEY}

    def get(self, request, *args, **kwargs):

        if not request.session['cart']['cart_count']:
            return redirect('/')
        return render(request, self.template_name, self.context)


class CheckoutChargeView(View):

    def post(self, request, *args, **kwargs):
        cart = request.session.get('cart', None)

        # make charge attempt
        try:
            token = request.POST['stripeToken']
            amount = int(cart['cart_total']) * 100
            charge = stripe.Charge.create(
                amount=amount,
                currency='eur',
                description='IssueTracker: Purchase of Feature Votes.',
                source=token,
            )

        # problem with the card
        except stripe.error.CardError:
            messages.error(request, "Your card was declined!")
            return redirect('/checkout/')

        # successful payment
        if charge.paid:
            for item in cart['cart_items']:
                ticket = get_object_or_404(Ticket, id=item['id'])
                user = self.request.user




