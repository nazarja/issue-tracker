from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.views.generic import View, ListView, TemplateView


class CartListView(View):
    template_name = 'cart/cart.html'
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)


class CartUpdateView(View):

    def post(self, request, *args, **kwargs):
        cart = request.session.get('cart', {'cart_items': [], 'cart_count': 0, 'cart_total': 0})

        print()
        cart_item = {
            'id': int(request.POST.get('id')),
            'votes': int(request.POST.get('votes')),
            'value': int(request.POST.get('value')),
            'timestamp': timezone.now().isoformat(),
        }
        cart['cart_items'].append(cart_item)
        request.session['cart'] = cart
        return JsonResponse({'cart': request.session['cart']})
