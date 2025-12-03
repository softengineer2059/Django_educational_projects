from django.db.models import Count, Q
from collections import Counter
import itertools
from .models import Product, ProductViewHistory, Product_image


class RecommendationService:

    @staticmethod
    def get_recommendations_for_product(product, limit=5):
        # Получить рекомендации для конкретного товара
        # Находим пользователей, которые смотрели этот товар
        product_viewers = ProductViewHistory.objects.filter(
            product=product
        ).values_list('user', 'session_key')

        user_ids = [viewer[0] for viewer in product_viewers if viewer[0]]
        session_keys = [viewer[1] for viewer in product_viewers if viewer[1]]

        # Находим другие товары, которые смотрели эти же пользователи
        related_views = ProductViewHistory.objects.filter(
            Q(user_id__in=user_ids) | Q(session_key__in=session_keys)
        ).exclude(product=product)

        # Группируем по товарам и считаем частоту
        product_counts = related_views.values('product').annotate(
            view_count=Count('product')
        ).order_by('-view_count')[:limit]

        product_ids = [item['product'] for item in product_counts]

        #product_img = Product_image.objects.filter(product__in=product_ids)

        return Product.objects.filter(id__in=product_ids).prefetch_related('images')

    @staticmethod
    def get_recommendations_for_user(user, session_key=None, limit=5):
        #Получить персонализированные рекомендации для пользователя
        if user.is_authenticated:
            user_views = ProductViewHistory.objects.filter(user=user)
        elif session_key:
            user_views = ProductViewHistory.objects.filter(session_key=session_key)
        else:
            return Product.objects.none()

        if not user_views.exists():
            # Если нет истории просмотров, возвращаем популярные товары
            return RecommendationService.get_popular_products(limit)

        # Получаем ID просмотренных товаров
        viewed_product_ids = user_views.values_list('product_id', flat=True)

        # Находим пользователей с похожей историей просмотров
        similar_users_views = ProductViewHistory.objects.filter(
            product_id__in=viewed_product_ids
        ).exclude(
            Q(user=user) if user.is_authenticated else Q(session_key=session_key)
        )

        if user.is_authenticated:
            similar_users = similar_users_views.filter(user__isnull=False).values_list('user', flat=True)
            recommendations = ProductViewHistory.objects.filter(
                user_id__in=similar_users
            ).exclude(product_id__in=viewed_product_ids)
        else:
            similar_sessions = similar_users_views.values_list('session_key', flat=True)
            recommendations = ProductViewHistory.objects.filter(
                session_key__in=similar_sessions
            ).exclude(product_id__in=viewed_product_ids)

        # Сортируем по популярности
        product_counts = recommendations.values('product').annotate(
            count=Count('product')
        ).order_by('-count')[:limit]

        product_ids = [item['product'] for item in product_counts]

        return Product.objects.filter(id__in=product_ids)

    @staticmethod
    def get_popular_products(limit=5):
        #Получить популярные товары
        popular_product_ids = ProductViewHistory.objects.values('product').annotate(
            view_count=Count('product')
        ).order_by('-view_count')[:limit].values_list('product_id', flat=True)

        return Product.objects.filter(id__in=popular_product_ids)