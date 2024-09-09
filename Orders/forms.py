from django import forms
from Customers.models import Address
from .models import Order
 

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['discount', 'description', 'status']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['state', 'city', 'postal_code', 'full_address', 'extra_description']