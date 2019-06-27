from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from .models import Profile
from .models import get_avatars_files


class ChangeAvatarView(View):
    template_name = 'profiles/change_avatar.html'
    context = {}
    path = '/static/img/avatars/'

    def get(self, request, *args, **kwargs):
        self.context['avatars'] = get_avatars_files()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Profile, user_id=request.user.id)
        obj.avatar = request.POST['url']
        obj.save()
        request.session['avatar'] = request.POST['url']
        return HttpResponse('Successfully Changed Avatar')



