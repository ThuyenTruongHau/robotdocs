from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


def role_required(allowed_roles):
    """
    Decorator để kiểm tra quyền của user
    allowed_roles: list các role được phép truy cập
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Bạn cần đăng nhập để truy cập trang này.')
                return redirect('core:admin_login')
            
            # Superuser luôn có quyền truy cập
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Lấy profile của user
            profile = getattr(request.user, 'profile', None)
            if not profile:
                messages.error(request, 'Thông tin tài khoản không hợp lệ.')
                return redirect('core:admin_login')
            
            # Kiểm tra role
            if profile.role not in allowed_roles:
                messages.error(request, 'Bạn không có quyền truy cập trang này.')
                return redirect('manage_category:admin_dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    """Decorator yêu cầu quyền admin"""
    return role_required(['admin'])(view_func)


def staff_required(view_func):
    """Decorator yêu cầu quyền staff trở lên"""
    return role_required(['admin', 'staff'])(view_func)


def superuser_required(view_func):
    """Decorator yêu cầu quyền superuser"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Bạn cần đăng nhập để truy cập trang này.')
            return redirect('core:admin_login')
        
        if not request.user.is_superuser:
            messages.error(request, 'Bạn cần quyền siêu quản trị để truy cập trang này.')
            return redirect('manage_category:admin_dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper
