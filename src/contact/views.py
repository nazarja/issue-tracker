from django.shortcuts import reverse
from django.views.generic import CreateView
from django.http import JsonResponse
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template


def send_email(name, email, subject):
    """
    helper function to send email using MailGun as the email sender
    emails failing must not affect page operation
    """
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
        """
        if it's a logged in user, set the initial data from their profile details
        other initial data should be blank
        """
        initial = super(ContactCreateView, self).get_initial()
        if self.request.user.is_authenticated:
            initial['name'] = self.request.user.username
            initial['email'] = self.request.user.email
        else:
            initial['name'] = ''
        return initial

    def form_valid(self, form):
        """
        if the form is valid, we should save the contact form model
        we then send an email to the users email address confirming success
        """
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            super(ContactCreateView, self).form_valid(form)
        else:
            super().form_valid(form)

        # send success email - call send_email function - pass in cleaned data from query dict
        send_email(form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['subject'])

        # send a json response back to the front end
        response = {
            'text': 'Your form has been successfully sent. Thank you.',
            'isAuth': True if self.request.user.is_authenticated else False
        }
        return JsonResponse(response)

    def form_invalid(self, form):
        """
        if the form is invalid we should inform the user of the error
        """
        super().form_invalid(form)
        response = {
            'text': 'An error has occurred, please try again later.',
            'error': form.errors
        }
        return JsonResponse(response, status=400)

    def get_success_url(self):
        return reverse('contact:contact')













