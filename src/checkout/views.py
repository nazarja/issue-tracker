from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.conf import settings
from django.contrib import messages
from .models import Order
from tickets.models import Ticket

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

            # create the order and save it before adding manytomany fields
            user = self.request.user
            votes = cart['cart_votes']
            total = cart['cart_total']
            order = Order.objects.create(user=user, votes=votes, total=total)
            order.save()

            # loop over all tickets in cart
            for item in cart['cart_items']:

                # increase tickets votes and add user to manytomany
                ticket = get_object_or_404(Ticket, id=item['id'])
                ticket.votes += item['votes']
                ticket.earned += item['value']
                ticket.vote_profiles.add(user)
                ticket.save()

                # add ticket to orders manytomany
                order.ticket.add(ticket)
                order.save()

            # reset cart to zero and redirect
            messages.success(request, "Thank you for your payment!")
            request.session['cart'] = {'cart_items': [], 'cart_count': 0, 'cart_votes': 0, 'cart_total': 0}
            return redirect('/checkout/payment-accepted/')
        else:
            messages.error(request, "We cant take payment right now, please try again later.")
            return redirect('/checkout/')


class CheckoutSuccessView(View):
    template_name = 'checkout/success.html'
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
