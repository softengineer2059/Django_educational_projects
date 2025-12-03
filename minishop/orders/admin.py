from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city', 'created', 'updated', 'paid']
    list_display_links = ['user', 'first_name', 'last_name']
    search_fields = ['user', 'first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city']


admin.site.register(Order, OrderAdmin)