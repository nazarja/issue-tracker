from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from .models import Profile
from .models import get_avatars_files


class ChangeAvatarView(View):
    """
    generic view for avatar gallery
    """
    template_name = 'profiles/change_avatar.html'
    context = {}
    path = '/static/img/avatars/'

    def get(self, request, *args, **kwargs):
        """
        on get, returns all avatars from helper function in models.py
        passes dict of avatar file paths to the context for display in html
        """
        self.context['avatars'] = get_avatars_files()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        """
        get the users profile, and save the new avatars file path
        """
        obj = get_object_or_404(Profile, user_id=request.user.id)
        obj.avatar = request.POST['url']
        obj.save()

        # session needs the avatar to display the avatar image in the navbar
        request.session['avatar'] = request.POST['url']
        return HttpResponse('Successfully Changed Avatar')



