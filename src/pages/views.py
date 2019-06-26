from django.shortcuts import render, redirect
from django.views import View
from profiles.models import Profile


class IndexView(View):
    template_name = 'pages/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

