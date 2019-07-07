from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    contact form inherits from contact model,
    need to set custom textarea for the message field
    """
    message = forms.CharField(max_length=2000, required=True, widget=forms.Textarea)

    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'subject',
            'message'
        ]