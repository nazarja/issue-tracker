from django.shortcuts import render, redirect
from django.views import View


class IndexView(View):
    """
    view to render the index page
    """
    template_name = 'pages/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        """
        if logged in your should not be able to see this page
        instead you should be redirect to the activity feed which serves as a home page for logged in users
        """
        if request.user.is_authenticated:
            return redirect('/activity-feed/')
        return render(request, self.template_name, self.context)





