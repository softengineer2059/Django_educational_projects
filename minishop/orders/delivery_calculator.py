from account.models import *


class DeliveryCalculator:
    @staticmethod
    def calculate_delivery_cost(vendor, region_name, cart_items_total):
        """Рассчитывает стоимость доставки для продавца и региона"""
        try:
            vendor_settings = VendorDeliverySettings.objects.get(vendor=vendor)

            # Проверяем бесплатную доставку
            if cart_items_total >= vendor_settings.free_delivery_threshold:
                return 0

            # Ищем цену для региона
            region_price = vendor_settings.region_prices.filter(
                region_name=region_name
            ).first()

            if region_price:
                return region_price.delivery_cost
            else:
                # Цена по умолчанию или обработка ошибки
                return 200  # или raise Exception

        except VendorDeliverySettings.DoesNotExist:
            # Настройки доставки не найдены
            return 300  # или стандартная цена


