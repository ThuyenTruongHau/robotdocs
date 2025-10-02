from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.generic import View
import logging

User = get_user_model()
logger = logging.getLogger("my_app_logger")


@csrf_protect
def admin_login(request):
    """Trang đăng nhập admin - Tối ưu tốc độ"""
    if request.user.is_authenticated:
        return redirect('manage_category:admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember = request.POST.get('remember')
        
        # Fast validation
        if not username or not password:
            messages.error(request, 'Vui lòng nhập đầy đủ thông tin đăng nhập.')
            return render(request, 'auth/login.html')
        
        # Optimized authentication
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            
            # Set session expiry based on remember me
            if remember:
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
            else:
                request.session.set_expiry(0)  # Browser session
            
            # Log login activity (async if possible)
            logger.info(f"User {user.username} logged in from {request.META.get('REMOTE_ADDR', 'Unknown')}")
            
            messages.success(request, f'Chào mừng {user.username}!')
            return redirect('manage_category:admin_dashboard')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
            logger.warning(f"Failed login attempt for {username} from {request.META.get('REMOTE_ADDR', 'Unknown')}")
    
    return render(request, 'auth/login.html')


@login_required(login_url='/auth/login/')
def admin_logout(request):
    """Đăng xuất admin"""
    username = request.user.username
    
    # Log logout activity
    logger.info(f"User {username} logged out from {request.META.get('REMOTE_ADDR', 'Unknown')}")
    
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất thành công.')
    return redirect('core:admin_login')




class AdminLoginView(View):
    """Class-based view cho đăng nhập admin"""
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('manage_category:admin_dashboard')
        return render(request, 'auth/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    # Log login activity
                    logger.info(f"User {user.username} logged in successfully from {request.META.get('REMOTE_ADDR', 'Unknown')}")
                    
                    # Set session expiry based on remember me
                    if remember:
                        request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
                    else:
                        request.session.set_expiry(0)  # Browser session
                    
                    messages.success(request, f'Chào mừng {user.username}! Đăng nhập thành công.')
                    return redirect('manage_category:admin_dashboard')
                else:
                    messages.error(request, 'Tài khoản của bạn đã bị vô hiệu hóa.')
                    logger.warning(f"Disabled user {username} attempted to log in from {request.META.get('REMOTE_ADDR', 'Unknown')}")
            else:
                messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
                logger.warning(f"Failed login attempt for username {username} from {request.META.get('REMOTE_ADDR', 'Unknown')}")
        else:
            messages.error(request, 'Vui lòng nhập đầy đủ thông tin đăng nhập.')
        
        return render(request, 'auth/login.html')


class AdminLogoutView(View):
    """Class-based view cho đăng xuất admin"""
    
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'auth/logout.html')
    
    @method_decorator(login_required)
    def post(self, request):
        username = request.user.username
        
        # Log logout activity
        logger.info(f"User {username} logged out from {request.META.get('REMOTE_ADDR', 'Unknown')}")
        
        logout(request)
        messages.success(request, 'Bạn đã đăng xuất thành công.')
        return redirect('core:admin_login')
