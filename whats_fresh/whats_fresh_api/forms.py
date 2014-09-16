import django.forms as forms
from whats_fresh.whats_fresh_api.models import *


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        widgets = {
            'name': forms.TextInput(attrs={'required':'true'}),
            'description': forms.TextInput(attrs={'required':'true'}),
            'hours': forms.TextInput,
            'street': forms.TextInput(attrs={'required':'true'}),
            'city': forms.TextInput(attrs={'required':'true'}),
            'state': forms.TextInput(attrs={'required':'true'}),
            'zip': forms.TextInput(attrs={'required':'true'}),
            'contact_name': forms.TextInput(attrs={'required':'true'}),
            'lat': forms.HiddenInput
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        widgets = {
                'name': forms.TextInput(attrs={'required':'true'}),
            'variety': forms.TextInput,
            'season': forms.TextInput(attrs={'required':'true'}),
            'origin': forms.TextInput,
            'alt_name': forms.TextInput,
            'description': forms.TextInput(attrs={'required':'true'}),
            'market_price': forms.TextInput(attrs={'required':'true'})
        }
        exclude = ('preparations',)


class PreparationForm(forms.ModelForm):
    class Meta:
        model = Preparation
        widgets = {
            'name': forms.TextInput(attrs={'required':'true'}),
            'additional_info': forms.TextInput,
            'description': forms.TextInput
        }
