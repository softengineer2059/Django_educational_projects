from django.db.models import Sum
from cart.models import Cart
from account.models import User_avatar
from magazine.models import Product_category, Product_subcategory
from orders.models import Order
from .services import RecommendationService


def recommendations(request):
    #Добавляет рекомендации в контекст всех шаблонов
    context = {}

    # Рекомендации для пользователя
    if request.user.is_authenticated:
        context['user_recommendations'] = RecommendationService.get_recommendations_for_user(
            request.user, limit=4
        )
    else:
        session_key = request.session.session_key
        if session_key:
            context['user_recommendations'] = RecommendationService.get_recommendations_for_user(
                None, session_key=session_key, limit=4
            )

    # Популярные товары (на случай если нет персонализированных рекомендаций)
    if 'user_recommendations' not in context or not context['user_recommendations']:
        context['user_recommendations'] = RecommendationService.get_popular_products(limit=4)

    return context


def cart_and_categories(request):
    if request.user.is_authenticated:
        cart_items_count = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        orders_count = Order.objects.filter(user=request.user).count() or 0
    else:
        cart_items_count = 0
        orders_count = 0
    category_list = Product_category.objects.values_list('id', 'category_name')
    subcategories_list = Product_subcategory.objects.values_list('id', 'subcategory_name', 'category_name')
    try:
        avatar = User_avatar.objects.get(user=request.user)
    except:
        avatar = False
    # Получаем историю переходов из сессии
    history = request.session.get('history', [])

    return {
        'orders_count': orders_count,
        'cart_items_count': cart_items_count,
        'category_list': category_list,
        'subcategories_list': subcategories_list,
        'history': history,
        'avatar': avatar
    }