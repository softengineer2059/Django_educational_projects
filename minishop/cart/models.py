from django.db import models
from django.contrib.auth.models import User
from magazine.models import Product




class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=300, blank=True, verbose_name='название продукта')
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    product = models.ForeignKey(Product, related_name='cart_product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} x {self.product}"