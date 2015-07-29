from django import forms
from django.conf import settings
# from whats_fresh import base
from django.utils.safestring import mark_safe


class ColorPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                # base.STATIC_URL + 'cssjs/colorPicker.css',
                'https://rawgit.com/laktek/really-simple-color-picker/master/css/colorPicker.css',  # noqa
            )
        }
        js = (
               'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
                # base.STATIC_URL + 'cssjs/jquery.colorPicker.js',
            'https://rawgit.com/laktek/really-simple-color-picker/master/js/jquery.colorPicker.js',  # noqa
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(ColorPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(ColorPickerWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $('#id_%s').colorPicker();
            </script>''' % name)
