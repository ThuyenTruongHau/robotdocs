"""
Hệ thống phân quyền thống nhất
Tập trung tất cả logic phân quyền tại đây
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

User = get_user_model()


class PermissionManager:
    """Quản lý phân quyền tập trung"""
    
    # Định nghĩa quyền cho từng role
    ROLE_PERMISSIONS = {
        'superuser': {
            'can_manage_users': True,
            'can_manage_categories': True,
            'can_manage_products': True,
            'can_view_dashboard': True,
            'can_manage_system': True,
        },
        'admin': {
            'can_manage_users': True,        # Chỉ admin mới quản lý users
            'can_manage_categories': True,
            'can_manage_products': True,
            'can_view_dashboard': True,
            'can_manage_system': False,
        },
        'staff': {
            'can_manage_users': False,       # Staff KHÔNG quản lý users
            'can_manage_categories': True,
            'can_manage_products': True,
            'can_view_dashboard': True,
            'can_manage_system': False,
        },
        'viewer': {
            'can_manage_users': False,
            'can_manage_categories': False,
            'can_manage_products': False,
            'can_view_dashboard': True,
            'can_manage_system': False,
        }
    }
    
    @classmethod
    def has_permission(cls, user, permission):
        """Kiểm tra user có quyền cụ thể không"""
        if not user.is_authenticated:
            return False
        
        # Superuser có tất cả quyền
        if user.is_superuser:
            return True
        
        # Lấy role từ profile
        role = getattr(user, 'profile', None)
        if not role:
            return False
        
        user_role = role.role
        permissions = cls.ROLE_PERMISSIONS.get(user_role, {})
        
        return permissions.get(permission, False)
    
    @classmethod
    def get_user_role(cls, user):
        """Lấy role của user"""
        if user.is_superuser:
            return 'superuser'
        
        profile = getattr(user, 'profile', None)
        return profile.role if profile else 'viewer'
    
    @classmethod
    def sync_django_permissions(cls, user):
        """Đồng bộ Django permissions với custom role"""
        if user.is_superuser:
            return  # Superuser không cần sync
        
        profile = getattr(user, 'profile', None)
        if not profile:
            return
        
        # Đồng bộ is_staff theo role
        if profile.role == 'admin':
            if not user.is_staff:
                user.is_staff = True
                user.save(update_fields=['is_staff'])
        elif profile.role == 'staff':
            # Staff không cần is_staff=True để xem menu Users
            if user.is_staff:
                user.is_staff = False
                user.save(update_fields=['is_staff'])
        else:
            # Các role khác không có is_staff
            if user.is_staff:
                user.is_staff = False
                user.save(update_fields=['is_staff'])


def permission_required(permission_name):
    """Decorator kiểm tra quyền cụ thể"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not PermissionManager.has_permission(request.user, permission_name):
                messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
                return redirect('manage_category:admin_dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def role_required(allowed_roles):
    """Decorator kiểm tra role (backward compatibility)"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Bạn cần đăng nhập để truy cập trang này.')
                return redirect('core:admin_login')
            
            user_role = PermissionManager.get_user_role(request.user)
            
            if user_role not in allowed_roles:
                messages.error(request, 'Bạn không có quyền truy cập trang này.')
                return redirect('manage_category:admin_dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# Backward compatibility decorators
def admin_required(view_func):
    """Decorator yêu cầu quyền admin"""
    return permission_required('can_manage_users')(view_func)


def staff_required(view_func):
    """Decorator yêu cầu quyền staff trở lên"""
    return role_required(['superuser', 'admin', 'staff'])(view_func)


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
