from django import template
from apps.core.permissions import PermissionManager

register = template.Library()


@register.filter
def has_permission(user, permission_name):
    """Template filter để kiểm tra quyền"""
    return PermissionManager.has_permission(user, permission_name)


@register.simple_tag
def user_role(user):
    """Template tag để lấy role của user"""
    return PermissionManager.get_user_role(user)


@register.inclusion_tag('admin/partials/permission_badge.html')
def permission_badge(user):
    """Template tag để hiển thị badge phân quyền"""
    role = PermissionManager.get_user_role(user)
    role_display = {
        'superuser': 'Siêu quản trị',
        'admin': 'Quản trị viên', 
        'staff': 'Nhân viên',
        'viewer': 'Người xem'
    }
    
    badge_colors = {
        'superuser': 'danger',
        'admin': 'warning',
        'staff': 'info',
        'viewer': 'secondary'
    }
    
    return {
        'role': role,
        'role_display': role_display.get(role, 'Không xác định'),
        'badge_color': badge_colors.get(role, 'secondary')
    }
