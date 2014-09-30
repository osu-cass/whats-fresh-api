from django.contrib.gis import admin
from whats_fresh.whats_fresh_api.models import *


class VendorProductInline(admin.TabularInline):
    model = VendorProduct
    extra = 2


class ImageAdmin(admin.GeoModelAdmin):
    readonly_fields = ('created', 'modified')


class VendorAdmin(admin.GeoModelAdmin):


    readonly_fields = ('created', 'modified')
    inlines = (VendorProductInline,)


class ProductAdmin(admin.GeoModelAdmin):
    readonly_fields = ('created', 'modified')
    inlines = (VendorProductInline,)


admin.site.register(Image, ImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Preparation)
admin.site.register(Story)
