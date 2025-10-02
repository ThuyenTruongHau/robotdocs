from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='user-register'),
    path('profile/', views.UserDetailView.as_view(), name='user-profile'),
    path('login/', views.login_view, name='user-login'),
    path('logout/', views.logout_view, name='user-logout'),
]
