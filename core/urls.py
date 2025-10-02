"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
   openapi.Info(
      title="Thado Robot API",
      default_version='v1',
      description="API documentation for Thado Robot project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@thadorobot.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def redirect_to_login(request):
    """Chuyển hướng root path đến trang đăng nhập"""
    return redirect('core:admin_login')

urlpatterns = [
    # Root path - Chuyển hướng đến trang đăng nhập
    path('', redirect_to_login, name='home'),
    
    # Authentication - Đặt trước admin để ưu tiên
    path('auth/', include('apps.core.auth_urls')),
    
    # Admin Panel - Custom admin interface
    path('manage/', include('apps.category.admin_urls')),
    path('manage/', include('apps.brand.admin_urls')),
    path('manage/', include('apps.product.admin_urls')),
    path('manage/', include('apps.core.admin_urls')),
    
    # API endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"), 
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/auth/', include('apps.users.urls')),
    path('api/', include('apps.category.urls')),
    path('api/', include('apps.product.urls')),
    path('api/', include('apps.brand.urls')),
    
    # Django Admin - Đặt cuối để không can thiệp vào custom admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
