import django.forms as forms
from whats_fresh.whats_fresh_api.models import (Vendor, Product, Preparation,
                                                Story, Video, Image, Theme)


class VendorForm(forms.ModelForm):

    class Meta:
        model = Vendor
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'required': 'true'}),
            'description': forms.Textarea(attrs={'required': 'true'}),
            'hours': forms.TextInput,
            'street': forms.TextInput(attrs={'required': 'true'}),
            'city': forms.TextInput(attrs={'required': 'true'}),
            'state': forms.TextInput(attrs={'required': 'true'}),
            'zip': forms.TextInput(attrs={'required': 'true'}),
            'contact_name': forms.TextInput(attrs={'required': 'true'}),
            'lat': forms.HiddenInput
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'required': 'true'}),
            'variety': forms.TextInput,
            'season': forms.TextInput(attrs={'required': 'true'}),
            'origin': forms.TextInput,
            'alt_name': forms.TextInput,
            'description': forms.Textarea(attrs={'required': 'true'}),
            'market_price': forms.TextInput(attrs={'required': 'true'})
        }
        exclude = ('preparations',)


class StoryForm(forms.ModelForm):

    class Meta:
        model = Story
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'required': 'true'}),
            'history': forms.Textarea,
            'buying': forms.Textarea,
            'preparing': forms.Textarea,
            'products': forms.Textarea,
            'season': forms.Textarea,
            'facts': forms.Textarea
        }
        exclude = ('preparations',)


class PreparationForm(forms.ModelForm):

    class Meta:
        model = Preparation
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'required': 'true'}),
            'additional_info': forms.TextInput,
            'description': forms.Textarea
        }


class VideoForm(forms.ModelForm):

    class Meta:
        model = Video
        exclude = []
        widgets = {
            'caption': forms.TextInput(attrs={'required': 'true'}),
            'name': forms.TextInput(attrs={'required': 'true'}),
            'video': forms.TextInput(attrs={'required': 'true'})
        }


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = []
        widgets = {
            'caption': forms.TextInput(attrs={'required': 'true'}),
            'name': forms.TextInput(attrs={'required': 'true'}),
            'image': forms.FileInput(attrs={'required': 'true'})
        }


class ThemeForm(forms.ModelForm):

    class Meta:
        model = Theme
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'required': 'true'}),
            'background_color': forms.TextInput,
            'foreground_color': forms.TextInput,
            'logo': forms.FileInput,
            'slogan': forms.TextInput,
            'site_title': forms.TextInput(attrs={'required': 'true'}),
            'vendors': forms.TextInput(attrs={'required': 'true'}),
            'vendors_slug': forms.TextInput(attrs={'required': 'true'}),
            'products': forms.TextInput(attrs={'required': 'true'}),
            'vendors_slug': forms.TextInput(attrs={'required': 'true'}),
            'vendors': forms.TextInput(attrs={'required': 'true'}),
            'vendors_slug': forms.TextInput(attrs={'required': 'true'}),
            'vendors': forms.TextInput(attrs={'required': 'true'}),
            'vendors_slug': forms.TextInput(attrs={'required': 'true'}),
            'vendors': forms.TextInput(attrs={'required': 'true'}),
            'vendors_slug': forms.TextInput(attrs={'required': 'true'}),
            'active': forms.TextInput

        }
