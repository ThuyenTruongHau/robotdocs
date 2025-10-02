# core/middlewares.py
import time
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
from .logger import logger

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        user = getattr(request, "user", None)
        user_info = user.username if user and user.is_authenticated else "Anonymous"

        logger.info(f"[REQUEST] {request.method} {request.get_full_path()} by {user_info}")

    def process_response(self, request, response):
        duration = None
        if hasattr(request, "start_time"):
            duration = round(time.time() - request.start_time, 3)

        logger.info(
            f"[RESPONSE] {request.method} {request.get_full_path()} "
            f"status={response.status_code} "
            f"duration={duration}s"
        )
        return response

    def process_exception(self, request, exception):
        logger.error(
            f"[EXCEPTION] {request.method} {request.get_full_path()} "
            f"error={str(exception)}"
        )


class CustomLoginRedirectMiddleware(MiddlewareMixin):
    """
    Middleware để chuyển hướng tất cả requests đến trang đăng nhập tùy chỉnh
    """
    
    def process_request(self, request):
        # Danh sách các đường dẫn được phép truy cập mà không cần đăng nhập
        allowed_paths = [
            '/auth/login/',  # Trang đăng nhập
            '/auth/logout/',  # Trang đăng xuất
            '/static/',  # Static files
            '/media/',  # Media files
            '/api/',  # API endpoints
            '/swagger/',  # Swagger documentation
            '/redoc/',  # ReDoc documentation
        ]
        
        # Kiểm tra xem đường dẫn hiện tại có được phép không
        current_path = request.path
        is_allowed = any(current_path.startswith(path) for path in allowed_paths)
        
        # Nếu không được phép và user chưa đăng nhập, chuyển hướng đến trang đăng nhập
        if not is_allowed and not request.user.is_authenticated:
            logger.info(f"[REDIRECT] Redirecting {request.method} {current_path} to custom login page")
            return redirect('core:admin_login')
        
        return None
