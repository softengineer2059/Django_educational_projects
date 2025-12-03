from django.urls import path
from comments import views




urlpatterns = [
    path('add_comment/<int:product_id>/', views.add_comment, name='add_comment'),
    path('comment_like_dislike/<int:comment_id>/<str:action>/', views.comment_add_like_dislike, name='comment_like_dislike'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('remove_comment/<slug:pk>/', views.Remove_comment.as_view(), name='remove_comment'),
    path('remove_editable_comment_image/<slug:pk>/', views.Remove_editable_comment_image.as_view(), name='remove_editable_comment_image'),
]