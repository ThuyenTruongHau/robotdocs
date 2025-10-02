from django.urls import path
from . import admin_views

app_name = 'manage_brand'

urlpatterns = [
    path('brands/', admin_views.brand_list, name='brand_list'),
    path('brands/create/', admin_views.brand_create, name='brand_create'),
    path('brands/<int:pk>/', admin_views.brand_detail, name='brand_detail'),
    path('brands/<int:pk>/edit/', admin_views.brand_edit, name='brand_edit'),
    path('brands/<int:pk>/delete/', admin_views.brand_delete, name='brand_delete'),
    path('brands/<int:brand_id>/products/create/', admin_views.brand_product_create, name='brand_product_create'),
]
