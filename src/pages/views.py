from django.shortcuts import render, redirect
from django.views import View


class IndexView(View):
    template_name = 'pages/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/activity-feed/')
        return render(request, self.template_name, self.context)

