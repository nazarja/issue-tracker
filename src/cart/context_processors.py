from django.shortcuts import get_object_or_404
from tickets.models import Ticket


def tickets_cart(request):
    cart = request.session.get('cart', {})

    items = []
    count = 0
    total_cost = 0
    total_votes = 0
    total_count = 0

    if not cart:
        return {'cart_items': [], 'cart_count': 0, 'cart_votes': 0, 'cart_total': 0}

    for item in cart['cart_items']:
        ticket = get_object_or_404(Ticket, id=item['id'])
        total = item['value']
        votes = item['votes']

        # main object stats
        total_cost += total
        total_votes += votes
        total_count += 1
        count += 1

        # single object return
        items.append({'id': item['id'], 'total': total, 'votes': votes, 'timestamp': item['timestamp'], 'ticket': ticket})

    # update session variable
    cart['cart_total'] = total_cost
    cart['cart_votes'] = total_votes
    cart['cart_count'] = total_count
    request.session['cart'] = cart

    # main return
    return {'cart_items': items, 'cart_count': count, 'cart_votes': total_votes, 'cart_total': total_cost}
