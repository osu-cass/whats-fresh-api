from django.contrib import admin
from whats_fresh.whats_fresh_api.models import Theme


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)


# Register your models here.

admin.site.register(Theme, ThemeAdmin)
