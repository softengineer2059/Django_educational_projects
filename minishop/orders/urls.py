from django.urls import path
from orders import views


urlpatterns = [
    path('orders_delete/<slug:pk>/', views.Delete_order.as_view(), name='orders_delete'),
    path('orders_detail/<int:id>/', views.Order_detail.as_view(), name='orders_detail'),
    path('create_order/', views.order_create, name="create_order"),
    path('orders_list/', views.orders_list, name="orders_list"),
    path('orders_checkout/', views.checkout, name='checkout'),
    ]