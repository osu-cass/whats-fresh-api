from django.db import models
from django.contrib import admin
from whats_fresh.whats_fresh_api.widgets import ColorPickerWidget
from whats_fresh.whats_fresh_api.models import Theme


class ThemeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': ColorPickerWidget},
    }
    list_display = ('name',)


# Register your models here.

admin.site.register(Theme, ThemeAdmin)
