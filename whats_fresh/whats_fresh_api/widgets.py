from django import forms
# from whats_fresh import base


class ColorPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                # base.STATIC_URL + 'css/spectrum.css',
                'https://rawgit.com/bgrins/spectrum/master/spectrum.css',  # noqa
            )
        }
        js = (
               'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # noqa
                # base.STATIC_URL + 'js/spectrum.js',
            # 'https://rawgit.com/bgrins/spectrum/master/spectrum.js',  # noqa
        )
