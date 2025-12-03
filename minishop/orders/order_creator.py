from .models import *
from .delivery_calculator import *


class OrderCreator:
    @staticmethod
    def create_order_from_cart(cart, user_data):
        """Создает заказ из корзины с разделением по продавцам"""
        # Группируем товары по продавцам
        vendor_items = {}
        for item in cart:
            vendor = item.product.vendor
            if vendor not in vendor_items:
                vendor_items[vendor] = []
            vendor_items[vendor].append(item)

        # Создаем родительский заказ
        order = Order.objects.create(
            user=user_data['user'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            address=user_data['address'],
            postal_code=user_data['postal_code'],
            city=user_data['city'],
        )

        # Создаем заказы для каждого продавца
        for vendor, items in vendor_items.items():
            items_cost = sum(item.product.discounted_price * item.quantity for item in items)
            delivery_cost = DeliveryCalculator.calculate_delivery_cost(
                vendor, user_data['city'], items_cost
            )

            vendor_order = VendorOrder.objects.create(
                parent_order=order,
                vendor=vendor,
                delivery_region=user_data['city'],
                delivery_cost=delivery_cost,
                items_cost=items_cost
            )

            # Создаем элементы заказа
            for item in items:
                OrderItem.objects.create(
                    vendor_order=vendor_order,
                    product=item.product,
                    price=item.product.discounted_price,
                    quantity=item.quantity
                )

        return order