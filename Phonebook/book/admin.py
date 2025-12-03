from django.contrib import admin
from .models import *


class departmentsAdmin(admin.ModelAdmin):
    list_display = ['department_name']
    list_display_links = ['department_name']
    search_fields = ['department_name']


class personnelAdmin(admin.ModelAdmin):
    list_display = ['employee_full_name', 'position', 'phone', 'mail', 'department']
    list_display_links = ['employee_full_name']
    search_fields = ['employee_full_name', 'position', 'phone']


admin.site.register(departments, departmentsAdmin)
admin.site.register(personnel, personnelAdmin)