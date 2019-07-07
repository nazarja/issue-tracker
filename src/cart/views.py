from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.utils import timezone


class CartListView(View):
    """
    returns cart html page
    """
    template_name = 'cart/cart.html'
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)


class CartCreateView(View):
    """
    only used for post requests, is called from javascript to
    add items to the cart, sets up the session 'cart'
    for the context processor on the next page refresh.
    """

    def post(self, request, *args, **kwargs):

        # get session 'cart' or create a default empty one
        cart = request.session.get('cart', {'cart_items': [], 'cart_count': 0, 'cart_votes': 0, 'cart_total': 0})

        # add item to cart list, timestamp will be a
        # unique identifier for duplicate votes (which are allowed)
        cart_item = {
            'id': int(request.POST.get('id')),
            'votes': int(request.POST.get('votes')),
            'value': int(request.POST.get('value')),
            'timestamp': timezone.now().isoformat(),
        }

        cart['cart_items'].append(cart_item)
        cart['cart_count'] += 1
        cart['cart_total'] += int(request.POST.get('value'))

        # assign back to session 'cart' and return response
        request.session['cart'] = cart
        return JsonResponse({'cart': request.session['cart']})


class CartUpdateView(View):
    """
    only used for post requests, is called from javascript to
    remove items to the cart, sets up the session 'cart'
    for the context processor on the next page refresh.
    """
    template_name = 'cart/cart.html'
    context = {}

    def post(self, request, *args, **kwargs):
        """
         a list of timestamps of still relevant cart items are posted from
         the front end, processed and sent back triggering a page refresh
        """
        cart = request.session.get('cart', None)
        tickets = request.POST.get('data').replace(' ', '+').split(',')

        # only add items to the cart if the timestamp is in the posted list,
        # otherwise they have been removed by the user
        cart['cart_items'] = [item for item in cart['cart_items'] if item['timestamp'] in tickets]

        # return session 'cart' and json response
        request.session['cart'] = cart
        return JsonResponse({'cart': request.session['cart']})
