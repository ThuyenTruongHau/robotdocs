from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SystemSettings(models.Model):
    """Model để lưu trữ cài đặt hệ thống"""
    key = models.CharField(max_length=100, unique=True, verbose_name="Khóa cài đặt")
    value = models.TextField(verbose_name="Giá trị")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cài đặt hệ thống"
        verbose_name_plural = "Cài đặt hệ thống"
        ordering = ['key']

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"


class UserProfile(models.Model):
    """Thông tin cơ bản của user"""
    ROLE_CHOICES = [
        ('admin', 'Quản trị viên'),
        ('staff', 'Nhân viên'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('it', 'Công nghệ thông tin'),
        ('hr', 'Nhân sự'),
        ('finance', 'Tài chính'),
        ('marketing', 'Marketing'),
        ('sales', 'Kinh doanh'),
        ('support', 'Hỗ trợ khách hàng'),
        ('other', 'Khác'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff', verbose_name="Vai trò")
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='other', verbose_name="Phòng ban")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """Tự động đồng bộ Django permissions khi lưu profile"""
        super().save(*args, **kwargs)
        self.sync_django_permissions()
    
    def sync_django_permissions(self):
        """Đồng bộ Django permissions theo role"""
        from .permissions import PermissionManager
        PermissionManager.sync_django_permissions(self.user)
    
    @classmethod
    def create_for_user(cls, user, role='staff', department='other'):
        """Tạo profile và đồng bộ permissions"""
        profile = cls.objects.create(
            user=user,
            role=role,
            department=department
        )
        profile.sync_django_permissions()
        return profile

    class Meta:
        verbose_name = "Hồ sơ người dùng"
        verbose_name_plural = "Hồ sơ người dùng"

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_role_display()})"
