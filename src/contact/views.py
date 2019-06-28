from django.shortcuts import reverse
from django.views.generic import CreateView
from django.http import JsonResponse
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template


def send_email(name, email, subject):
    send_mail(
        'Contact Form Submission',
        get_template('contact/email/contact-form-reply.html')
        .render(
            {
                "name": name,
                "subject": subject,
            }
        ),
        settings.EMAIL_MAIN, [email], fail_silently=True
    )


class ContactCreateView(CreateView):
    template_name = 'contact/contact.html'
    form_class = ContactForm

    def get_initial(self):
        initial = super(ContactCreateView, self).get_initial()
        if self.request.user.is_authenticated:
            initial['name'] = self.request.user.username
            initial['email'] = self.request.user.email
        else:
            initial['name'] = ''
        return initial

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            super(ContactCreateView, self).form_valid(form)
        else:
            super().form_valid(form)

        send_email(form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['subject'])

        response = {
            'text': 'Your form has been successfully sent. Thank you.',
            'isAuth': True if self.request.user.is_authenticated else False
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













