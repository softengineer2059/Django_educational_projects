from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_details', 'category', 'sub_category', 'created']
    list_display_links = ['product_name']
    search_fields = ['product_name', 'product_details']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    list_display_links = ['category_name']
    search_fields = ['category_name']


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['subcategory_name', 'category_name']
    list_display_links = ['subcategory_name']
    search_fields = ['subcategory_name']


class ProductOffer_admin(admin.ModelAdmin):
    list_display = ['product', 'vendor']
    list_display_links = ['product', 'vendor']
    search_fields = ['product', 'vendor']


class ProductViewHistory_admin(admin.ModelAdmin):
    list_display = ['user', 'product']
    list_display_links = ['user', 'product']
    search_fields = ['user', 'product']


class Product_image_admin(admin.ModelAdmin):
    list_display = ['product', 'image']
    list_display_links = ['product']
    search_fields = ['product__product_name']


admin.site.register(Product, ProductAdmin)
admin.site.register(Product_category, CategoryAdmin)
admin.site.register(Product_subcategory, SubcategoryAdmin)
admin.site.register(Product_image, Product_image_admin)
admin.site.register(ProductOffer, ProductOffer_admin)
admin.site.register(ProductViewHistory, ProductViewHistory_admin)