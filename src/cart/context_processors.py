from django.shortcuts import get_object_or_404
from tickets.models import Ticket


def tickets_cart(request):
    """
    Learned form CI videos
    Create a custom context processor to be available on all pages as 'cart' context
    On each page refresh a new updated cart is created. If cart does not exist and empty
    cart is returned to prevent any reference errors.
    """
    cart = request.session.get('cart', {})

    items = []
    count = 0
    total_cost = 0
    total_votes = 0
    total_count = 0

    if not cart:
        # if cart does not exist return any  default empty context
        return {'cart_items': [], 'cart_count': 0, 'cart_votes': 0, 'cart_total': 0}

    # get cart items by id
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

    # session 'cart' should be the same to avoid errors
    # on updating cart items before the next refresh
    request.session['cart'] = cart

    # main return
    return {'cart_items': items, 'cart_count': count, 'cart_votes': total_votes, 'cart_total': total_cost}
