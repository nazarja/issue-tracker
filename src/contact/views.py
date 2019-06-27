from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .forms import ContactForm


class ContactView(View):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.context['form'] = self.form_class(initial={'name': request.user.username, 'email': request.user.email})
        else:
            self.context['form'] = self.form_class
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        return HttpResponse('Email Sent Successfully.')
