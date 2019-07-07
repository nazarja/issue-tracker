from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    """
    inherits from ticket modal to create a form,
    most fields are left out and fields saved on the view / serializer
    description field needs a custom textarea field
    """
    description = forms.CharField(max_length=2000, required=True, widget=forms.Textarea)

    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'status',
        ]

