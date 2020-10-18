from django.views.generic import ListView
from tickets.models import Ticket
from comments.models import Comment
from checkout.models import Order
from profiles.models import Profile
from itertools import chain


class ActivityFeedListView(ListView):
    """
    Gather an object list of the most recent actions by users,
    present as two separate tabs, current user and other users.
    """
    template_name = 'activity_feed/feed.html'
    extra_context = {}

    def get_queryset(self):
        user = self.request.user

        try:
            # call the model managers to query their models
            tickets_list = Ticket.objects.get_latest(user)
            comments_list = Comment.objects.get_latest(user)
            order_list = Order.objects.get_latest(user)
            profiles_list = Profile.objects.get_latest(user)

            # chain together all object lists to return a single object list
            queryset_chain = chain(tickets_list, comments_list, order_list, profiles_list)

            # sort the queryset by created on date to be on top
            queryset = sorted(queryset_chain, key=lambda instance: instance.created_on, reverse=True)
            return queryset

        # if there's a problem return empty queryset
        except LookupError:
            return Profile.objects.none()


