from django import forms
from whats_fresh import base
from django.utils.safestring import mark_safe


class ColorPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                base.STATIC_URL + 'css/spectrum.css',
                # 'https://rawgit.com/bgrins/spectrum/master/spectrum.css',  # noqa
            )
        }
        js = (
               'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # noqa
                base.STATIC_URL + 'js/spectrum.js',
            # 'https://rawgit.com/bgrins/spectrum/master/spectrum.js',  # noqa
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or base.LANGUAGE_CODE[:2]
        super(ColorPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(ColorPickerWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $('#id_%s').spectrum();
            </script>''' % name)
