from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('date',)


# class PaymentForm(forms.Form):
#     credit_card_number = forms.CharField(max_length=19, label='Credit card number', required=True)
#     cvv = forms.CharField(max_length=3, label='Security code (CVV)', required=True)
#     expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES, required=False)
#     expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES, required=False)
#     stripe_id = forms.CharField(widget=forms.HiddenInput)
#
#     def clean_credit_card_number(self):
#         data = self.cleaned_data['cvv']
#
#         if not data.isdigit():
#             raise forms.ValidationError("The credit card number must only contain numbers")
#         return data
#
#     def clean_cvv(self):
#         data = self.cleaned_data['cvv']
#
#         if not data.isdigit():
#             raise forms.ValidationError("The CVV must only contain numbers")
#         return data
