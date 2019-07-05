from django import forms
from .models import Order

MONTH_CHOICES = [(i, i) for i in range(1, 13)]
YEAR_CHOICES = [(i, i) for i in range(2019, 2036)]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class PaymentForm(forms.Form):
    credit_card_number = forms.CharField(label='Credit card number', required=False)
    cvv = forms.CharField(label='Security code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)

