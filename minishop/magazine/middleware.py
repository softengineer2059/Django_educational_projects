from django.utils.deprecation import MiddlewareMixin
from .models import Product, ProductViewHistory


class ProductViewMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/product_detail/') and request.method == 'GET':
            product_id = request.path.split('/')[-2]
            if product_id.isdigit() and request.user.is_authenticated:
                try:
                    product = Product.objects.get(id=int(product_id))

                    # Убедимся, что у анонимного пользователя есть сессия
                    if not request.user.is_authenticated:
                        if not request.session.session_key:
                            request.session.create()  # Создаем сессию если её нет

                    # Сохраняем просмотр
                    view_history = ProductViewHistory(
                        product=product,
                        user=request.user if request.user.is_authenticated else None,
                        session_key=request.session.session_key if not request.user.is_authenticated else None
                    )
                    view_history.save()

                except Product.DoesNotExist:
                    pass
        return None