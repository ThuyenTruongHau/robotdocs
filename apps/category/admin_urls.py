from django.urls import path
from . import admin_views

app_name = 'manage_category'

urlpatterns = [
    path('', admin_views.admin_dashboard, name='admin_dashboard'),
    path('categories/', admin_views.category_list, name='category_list'),
    path('categories/create/', admin_views.category_create, name='category_create'),
    path('categories/<int:pk>/', admin_views.category_detail, name='category_detail'),
    path('categories/<int:pk>/edit/', admin_views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', admin_views.category_delete, name='category_delete'),
    path('categories/<int:category_id>/products/create/', admin_views.category_product_create, name='category_product_create'),
]
