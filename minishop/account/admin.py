from django.contrib import admin
from .models import *


class VendorAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'is_approved', 'created_at']
    list_display_links = ['company_name', 'is_approved', 'created_at']
    search_fields = ['user__username', 'company_name']  # указание поля связанной модели
    list_filter = ['is_approved', 'created_at']  # Добавьте фильтры


class VendorWarehouseAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'name', 'address', 'city', 'is_default']
    list_display_links = ['vendor', 'name', 'address', 'city', 'is_default']
    search_fields = ['vendor__company_name', 'name', 'address', 'city']


class VendorDeliverySettingsAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'free_delivery_threshold']
    list_display_links = ['vendor', 'free_delivery_threshold']
    search_fields = ['vendor__company_name']

    """def display_delivery_regions(self, obj):
        return ", ".join(obj.delivery_regions) if obj.delivery_regions else "Не указаны"

    display_delivery_regions.short_description = "Регионы доставки"""


class RegionDeliveryPriceAdmin(admin.ModelAdmin):
    list_display = ['vendor_settings', 'region_name', 'delivery_cost']
    list_display_links = ['vendor_settings', 'region_name', 'delivery_cost']
    search_fields = ['vendor_settings']


admin.site.register(Vendor, VendorAdmin)
admin.site.register(VendorWarehouse, VendorWarehouseAdmin)
admin.site.register(VendorDeliverySettings, VendorDeliverySettingsAdmin)
admin.site.register(RegionDeliveryPrice, RegionDeliveryPriceAdmin)