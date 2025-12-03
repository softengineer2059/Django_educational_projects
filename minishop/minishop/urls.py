from django.contrib import admin
from django.urls import path, include
from magazine import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('account/', include('account.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('comments/', include('comments.urls')),
    path('category_list/delete_category/<slug:pk>/', views.Delete_category.as_view(), name='delete_category'),
    path('subcategory_list/delete_subcategory/<slug:pk>/', views.Delete_subcategory.as_view(), name='delete_subcategory'),
    path("edit_product/<slug:pk>/", views.Edit_product.as_view(), name="edit_product"),
    path("delete_product/<slug:pk>/", views.Delete_product.as_view(), name="delete_product"),
    path('delete_editable_product_image/<slug:pk>/', views.Delete_editable_product_image.as_view(), name="delete_edit_prod_img"),
    path('product_detail/<int:id>/', views.Product_detail.as_view(), name='product_detail'),
    path("create_product/", views.Create_product.as_view(), name='create_product'),
    path("create_category/", views.create_category, name='create_category'),
    path("create_subcategory/", views.create_subcategory, name='create_subcategory'),
    path('category_list/', views.Category_list.as_view(), name='category_list'),
    path('subcategory_list/', views.Subcategory_list.as_view(), name='subcategory_list'),
    path('admin/', admin.site.urls),
    path('', views.Main.as_view(), name="main"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)