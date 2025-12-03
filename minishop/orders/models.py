from django.db import models
from magazine.models import Product
from django.contrib.auth.models import User
from account.models import *


class Order(models.Model):
    """Родительский заказ (корзина пользователя)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)  # Город доставки
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    # Общая стоимость (рассчитывается динамически)
    @property
    def get_total_cost(self):
        return sum(vendor_order.get_total_cost() for vendor_order in self.vendor_orders.all())

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'


class VendorOrder(models.Model):
    """Заказ для конкретного продавца"""
    ORDER_STATUS = (
        ('pending', 'Ожидает обработки'),
        ('confirmed', 'Подтвержден'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    )

    parent_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='vendor_orders')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    # Данные доставки для этого продавца
    delivery_region = models.CharField(max_length=100)  # Регион доставки
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Статус заказа у продавца
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')

    # Стоимость товаров (без доставки)
    items_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_total_cost(self):
        """Общая стоимость заказа у продавца (товары + доставка)"""
        return self.items_cost + self.delivery_cost

    def __str__(self):
        return f'VendorOrder {self.id} for {self.vendor.company_name}'


class OrderItem(models.Model):
    """Элементы заказа (привязываются к VendorOrder)"""
    vendor_order = models.ForeignKey(VendorOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return str(self.id)