"""from django import forms
from .models import ShipmentAddress


class AddressForm(forms.ModelForm):
    class Meta:
        #generate a form for a specific model
        model = ShipmentAddress
        fields = ["address_1", "address_2", "zip_code", "city", "country"]

class loginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
"""