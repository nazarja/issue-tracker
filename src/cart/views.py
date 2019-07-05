from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.utils import timezone


class CartListView(View):
    template_name = 'cart/cart.html'
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)


class CartCreateView(View):

    def post(self, request, *args, **kwargs):
        cart = request.session.get('cart', {'cart_items': [], 'cart_count': 0, 'cart_total': 0})

        cart_item = {
            'id': int(request.POST.get('id')),
            'votes': int(request.POST.get('votes')),
            'value': int(request.POST.get('value')),
            'timestamp': timezone.now().isoformat(),
        }
        cart['cart_items'].append(cart_item)
        request.session['cart'] = cart
        return JsonResponse({'cart': request.session['cart']})


class CartUpdateView(View):
    template_name = 'cart/cart.html'
    context = {}

    def post(self, request, *args, **kwargs):
        cart = request.session.get('cart', None)
        tickets = request.POST.get('data').replace(' ', '+').split(',')
        cart['cart_items'] = [item for item in cart['cart_items'] if item['timestamp'] in tickets]
        request.session['cart'] = cart
        return JsonResponse({'cart': request.session['cart']})
