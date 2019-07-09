from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Contact
from .forms import ContactForm
from django.urls import reverse


class TestContactViews(TestCase):
    """
    test contact views
    """
    def setUp(self):
        self.client = Client()
        self.page_url = reverse('contact:contact')

    def test_contact_get(self):
        response = self.client.get(self.page_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_contact_post(self):
        response = self.client.post(self.page_url, {
            'name': 'sean',
            'email': 'sean@sean.com',
            'subject': 'test case post',
            'message': 'This is a test'
        })

        obj = Contact.objects.get(email='sean@sean.com')
        self.assertEqual(obj.name, 'sean')


class TestContactForm(TestCase):
    """
    test contact forms
    """
    def test_form_valid(self):
        name = "test"
        email = 'test@test.com'
        subject = 'test contact form subject'
        message = 'test contact form message'

        user = User(id=1)
        user.save()

        obj = Contact.objects.create(user=user, name=name, email=email, subject=subject, message=message)
        data = {'name': obj.name, 'email': obj.email, 'subject': obj.subject, 'message': obj.message}
        form = ContactForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('subject'), obj.subject)
        self.assertNotEqual(form.cleaned_data.get('message'), 'test contact message')

    def test_form_invalid(self):
        name = "test"
        email = 'test@test.com'
        subject = 'test contact form subject'
        message = 'test contact form message'

        user = User(id=1)
        user.save()

        obj = Contact.objects.create(user=user, name=name, email=email, subject=subject, message=message)
        data = {'name': obj.name, 'email': obj.email, 'subject': obj.subject, 'message': ''}
        form = ContactForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
