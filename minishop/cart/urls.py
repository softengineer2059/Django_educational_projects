from django.urls import path
from cart import views




urlpatterns = [
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:cart_item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("update_cart_item/<int:product_id>/<str:action>/", views.update_cart_item, name="update_cart_item"),
    path("", views.cart_detail, name="cart")
    ]