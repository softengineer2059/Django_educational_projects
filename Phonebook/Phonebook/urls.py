from django.contrib import admin
from django.urls import path
from book import views


urlpatterns = [
    path('administration/admin_departments/<slug:pk>/', views.Admin_departments.as_view(), name='admin_departments'),
    path('administration/edit_adm_personnel/<slug:pk>/', views.Edit_adm_personnel.as_view(), name="edit_adm_personnel"),
    path('administration/delete_adm_departments/<slug:pk>/', views.Delete_adm_departments.as_view(), name='delete_adm_departments'),
    path('administration/delete_adm_personnel/<slug:pk>/', views.Delete_adm_personnel.as_view(), name='delete_adm_personnel'),
    path('administration/create_adm_personnel/', views.Create_adm_personnel.as_view(), name='create_adm_personnel'),
    path('administration/create_dep_departments/', views.Create_adm_departments.as_view(), name='create_adm_departments'),
    path('administration/search_admin_personnel/', views.Search.as_view(), {'base': 'admin_personnel'}, name='search_admin_personnel'),
    path('edit_dep_personnel/<slug:pk>/', views.Edit_dep_personnel.as_view(), name="edit_dep_personnel"),
    path('delete_dep_personnel/<slug:pk>/', views.Delete_dep_personnel.as_view(), name='delete_dep_personnel'),
    path('delete_dep_departments/<slug:pk>/', views.Delete_dep_departments.as_view(), name='delete_dep_department'),
    path('departments/<slug:pk>/', views.Departments.as_view(), name='departments'),
    path('administration/', views.Administration.as_view(), name='administration'),
    path('search_personnel/', views.Search.as_view(), {'base': 'personnel'}, name='search_personnel'),
    path('create_dep_personnel/', views.Create_dep_personnel.as_view(), name='create_dep_personnel'),
    path('create_dep_departments/', views.Create_dep_departments.as_view(), name='create_dep_departments'),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('admin/', admin.site.urls),
    path('', views.Main.as_view(), name='main'),
]
