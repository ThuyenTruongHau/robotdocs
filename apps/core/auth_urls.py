from django.urls import path
from . import auth_views

app_name = 'core'

urlpatterns = [
    path('login/', auth_views.admin_login, name='admin_login'),
    path('logout/', auth_views.admin_logout, name='admin_logout'),
]
