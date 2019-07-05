from django.views.generic import ListView
from tickets.models import Ticket
from comments.models import Comment
from checkout.models import Order
from profiles.models import Profile
from itertools import chain


class ActivityFeedListView(ListView):
    template_name = 'activity_feed/feed.html'
    extra_context = {}

    def get_queryset(self):
        user = self.request.user
        tickets_list = Ticket.objects.get_tickets(user)
        comments_list = Comment.objects.get_comments(user)
        order_list = Order.objects.get_orders(user)
        profiles_list = Profile.objects.get_profiles()


