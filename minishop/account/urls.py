from django.urls import path
from account import views


urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path('register/', views.Register.as_view(), name="register"),
    path("profile/", views.Account.as_view(), name="profile"),
    path('change_base_info/', views.change_base_info, name='change_base_info'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('upload_avatar/', views.upload_avatar_image, name='upload_avatar'),
    path('become-vendor/', views.become_vendor, name='become_vendor'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('warehouse/add/', views.change_vendorwarehouse_info, name='add_warehouse'),
    path('warehouse/edit_warehouse/<int:warehouse_id>/', views.change_vendorwarehouse_info, name='edit_warehouse'),
    path('warehouse/delete/<slug:pk>/', views.Delete_Warehouse.as_view(), name='delete_warehouse'),
    path('add_delivery/', views.vendor_delivery_settings, name='add_delivery'),
    path('edit_vendor_base_info/<slug:pk>/', views.Edit_vendor_base_info.as_view(), name='edit_base_info'),
    path('vendor_shop/<int:id>/', views.Vendor_product.as_view(), name='vendor_shop')
]