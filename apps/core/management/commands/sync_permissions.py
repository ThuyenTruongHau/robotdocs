from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import UserProfile
from apps.core.permissions import PermissionManager

User = get_user_model()


class Command(BaseCommand):
    help = 'Đồng bộ Django permissions với custom roles'

    def handle(self, *args, **options):
        self.stdout.write('Bắt đầu đồng bộ permissions...')
        
        # Đồng bộ tất cả users có profile
        users_with_profile = User.objects.filter(profile__isnull=False)
        updated_count = 0
        
        for user in users_with_profile:
            old_is_staff = user.is_staff
            PermissionManager.sync_django_permissions(user)
            user.refresh_from_db()
            
            if old_is_staff != user.is_staff:
                updated_count += 1
                self.stdout.write(
                    f'User "{user.username}": is_staff {old_is_staff} -> {user.is_staff}'
                )
        
        # Tạo profile cho users chưa có
        users_without_profile = User.objects.filter(profile__isnull=True)
        created_count = 0
        
        for user in users_without_profile:
            if not user.is_superuser:  # Không tạo profile cho superuser
                UserProfile.create_for_user(user, role='staff')
                created_count += 1
                self.stdout.write(f'Tạo profile cho user "{user.username}"')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Hoàn thành! Đã cập nhật {updated_count} users và tạo {created_count} profiles mới.'
            )
        )
