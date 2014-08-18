import django.forms as forms
from whats_fresh_api.models import *


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        widgets = {
            'name': forms.TextInput,
            'description': forms.TextInput,
            'street': forms.TextInput,
            'city': forms.TextInput,
            'state': forms.TextInput,
            'zip': forms.TextInput,
            'contact_name': forms.TextInput,
            'products': forms.HiddenInput
        }
