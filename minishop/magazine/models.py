from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from account.models import *


class Product_category(models.Model):

    category_name = models.CharField(max_length=150, null=True, verbose_name='категория')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        managed = True

    def __str__(self):
        return self.category_name


class Product_subcategory(models.Model):

    subcategory_name = models.CharField(max_length=150, null=True, verbose_name='подкатегория')
    category_name = models.ForeignKey(Product_category, null=True, verbose_name="Категория", on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'подкатегория'
        verbose_name_plural = 'подкатегории'
        managed = True

    def __str__(self):
        return self.subcategory_name


class Product(models.Model):

    product_name = models.CharField(max_length=300, blank=True, verbose_name='название продукта')
    product_details = models.CharField(blank=True, verbose_name='описание продукта')
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость товара')
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Скидочная цена')
    category = models.ForeignKey(Product_category, null=True, verbose_name='категория', on_delete=models.SET_NULL)
    sub_category = models.ForeignKey(Product_subcategory, null=True, verbose_name='подкатегория', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='дата создания')
    vendor = models.ForeignKey(Vendor, verbose_name="продавец", on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)  # Модерация товара

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'id': self.id})


class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(VendorWarehouse, on_delete=models.CASCADE)
    vendor_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


class Product_image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='product_images/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])

    def __str__(self):
        return f"Image for {self.product.product_name}"  # Это для красивого отображения


class ProductViewHistory(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар')
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name='дата просмотра')
    session_key = models.CharField(max_length=40, null=True, blank=True, verbose_name='ключ сессии')  # для анонимных пользователей

    class Meta:
        verbose_name = 'история просмотров'
        verbose_name_plural = 'истории просмотров'
        ordering = ('-viewed_at',)
        indexes = [
            models.Index(fields=['user', 'viewed_at']),
            models.Index(fields=['session_key', 'viewed_at']),
        ]

    def __str__(self):
        return f'{self.user} - {self.product}'