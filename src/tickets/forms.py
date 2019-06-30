from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    description = forms.CharField(max_length=2000, required=True, widget=forms.Textarea)

    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'status',
        ]

