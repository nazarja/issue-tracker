from django.shortcuts import render, redirect
from django.views import View


class IndexView(View):
    template_name = 'pages/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass  # put redirect so cant be on the index page
        return render(request, self.template_name, self.context)

