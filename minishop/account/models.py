from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class User_avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True, upload_to='users_avatar/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])

    def get_absolute_url(self):
        return self.img.url if self.img else ''

    #можно использовать в шаблоне вот так src="{{ avatar.get_absolute_url }}"


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    phone_number = models.CharField(max_length=40, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Электронная почта', max_length=255, blank=True)
    address = models.TextField()
    logo = models.ImageField(upload_to='vendors/')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class VendorWarehouse(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)


class VendorDeliverySettings(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    free_delivery_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class RegionDeliveryPrice(models.Model):
    vendor_settings = models.ForeignKey(VendorDeliverySettings, on_delete=models.CASCADE, related_name='region_prices')
    region_name = models.CharField(max_length=100, verbose_name='Название региона')
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость доставки')

    class Meta:
        unique_together = ['vendor_settings', 'region_name']
        verbose_name = 'Цена доставки по региону'
        verbose_name_plural = 'Цены доставки по регионам'

    def __str__(self):
        return f"{self.region_name} - {self.delivery_cost} руб."