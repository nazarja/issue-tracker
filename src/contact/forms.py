from django import forms
from .models import ContactFormModel


class ContactForm(forms.ModelForm):
    message = forms.CharField(max_length=2000, required=True, widget=forms.Textarea)

    class Meta:
        model = ContactFormModel
        fields = [
            'name',
            'email',
            'subject',
            'message'
        ]
