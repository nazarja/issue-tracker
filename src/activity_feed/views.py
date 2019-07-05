from django.shortcuts import render
from django.views.generic import View


class ActivityFeedListView(View):
    template_name = 'activity_feed/feed.html'
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
