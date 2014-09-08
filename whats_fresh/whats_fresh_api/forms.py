import django.forms as forms
from whats_fresh_api.models import *


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        widgets = {
            'name': forms.TextInput,
            'description': forms.TextInput,
            'hours': forms.TextInput,
            'street': forms.TextInput,
            'city': forms.TextInput,
            'state': forms.TextInput,
            'zip': forms.TextInput,
            'contact_name': forms.TextInput,
            'lat': forms.HiddenInput
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        widgets = {
            'name': forms.TextInput,
            'variety': forms.TextInput,
            'season': forms.TextInput,
            'origin': forms.TextInput,
            'alt_name': forms.TextInput,
            'description': forms.TextInput,
            'market_price': forms.TextInput
        }
        exclude = ('preparations',)


class PreparationForm(forms.ModelForm):
    class Meta:
        model = Preparation
        widgets = {
            'name': forms.TextInput,
            'additional_info': forms.TextInput,
            'description': forms.TextInput
        }
