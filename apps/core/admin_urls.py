from django.urls import path
from . import admin_views

app_name = 'manage_core'

urlpatterns = [
    path('users/', admin_views.user_list, name='user_list'),
    path('users/create/', admin_views.user_create, name='user_create'),
    path('users/<int:pk>/', admin_views.user_detail, name='user_detail'),
    path('users/<int:pk>/edit/', admin_views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', admin_views.user_delete, name='user_delete'),
    path('profile/', admin_views.user_profile, name='user_profile'),
]
