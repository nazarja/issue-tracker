from django.shortcuts import reverse
from django.views.generic import CreateView
from django.http import JsonResponse
from .forms import ContactForm


class ContactCreateView(CreateView):
    template_name = 'contact/contact.html'
    form_class = ContactForm

    def get_initial(self):
        initial = super(ContactCreateView, self).get_initial()
        if self.request.user.is_authenticated:
            initial['name'] = self.request.user.username
            initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        print('VALID')
        super().form_valid(form)
        response = {
            'text': 'Your form has been successfully sent. Thank you.',
        }
        return JsonResponse(response)

    def form_invalid(self, form):
        super().form_invalid(form)
        response = {
            'text': 'An error has occurred, please try again later.',
            'error': form.errors
        }
        return JsonResponse(response, status=400)

    def get_success_url(self):
        return reverse('contact:contact')













