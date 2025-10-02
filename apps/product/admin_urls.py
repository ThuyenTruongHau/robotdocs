from django.urls import path
from . import admin_views

app_name = 'manage_product'

urlpatterns = [
    path('products/', admin_views.product_list, name='product_list'),
    path('products/create/', admin_views.product_create, name='product_create'),
    path('products/<int:pk>/', admin_views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', admin_views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', admin_views.product_delete, name='product_delete'),
    path('products/<int:product_pk>/images/add/', admin_views.product_image_add, name='product_image_add'),
    path('images/<int:pk>/delete/', admin_views.product_image_delete, name='product_image_delete'),
]
