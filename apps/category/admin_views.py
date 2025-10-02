from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category
from .forms import CategoryForm
from apps.core.mixins import AdminListMixin


@login_required(login_url='/auth/login/')
def admin_dashboard(request):
    """Trang chủ quản trị"""
    from apps.product.models import Product
    from apps.brand.models import Brand
    from apps.core.models import UserProfile
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    categories_count = Category.objects.count()
    products_count = Product.objects.count()
    brand_count = Brand.objects.count()
    users_count = User.objects.count()
    active_users_count = User.objects.filter(is_active=True).count()
    
    # Đọc hoạt động gần đây từ log file với phân trang
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except:
        page = 1
    
    activities_data = get_recent_activities(page=page, per_page=6)
    
    context = {
        'categories_count': categories_count,
        'products_count': products_count,
        'users_count': users_count,
        'brand_count': brand_count,
        'active_users_count': active_users_count,
        'recent_activities': activities_data['activities'],
        'activities_pagination': activities_data,
    }
    return render(request, 'admin/dashboard.html', context)


def get_recent_activities(page=1, per_page=6):
    """Đọc hoạt động gần đây từ log file với phân trang"""
    import os
    from datetime import datetime, timedelta
    from django.core.paginator import Paginator
    
    log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs', 'app.log')
    activities = []
    
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Lấy 24 dòng cuối cùng (4 trang x 6 log)
            recent_lines = lines[-24:] if len(lines) > 24 else lines
            
            for line in recent_lines:
                # Parse log line để lấy thông tin hoạt động
                if 'INFO' in line and any(keyword in line for keyword in ['created', 'updated', 'deleted', 'viewed', 'POST', 'GET']):
                    try:
                        # Extract timestamp
                        timestamp_str = line.split(']-[')[0].replace('[', '')
                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        
                        # Extract message
                        message = line.split(']-')[2].strip() if ']-' in line else line.strip()
                        
                        # Determine action type
                        action_icon = 'fas fa-plus-circle text-success'
                        action_text = 'Tạo mới'
                        
                        if 'updated' in message.lower() or 'PUT' in message:
                            action_icon = 'fas fa-edit text-warning'
                            action_text = 'Cập nhật'
                        elif 'deleted' in message.lower() or 'DELETE' in message:
                            action_icon = 'fas fa-trash text-danger'
                            action_text = 'Xóa'
                        elif 'viewed' in message.lower() or 'GET' in message:
                            action_icon = 'fas fa-eye text-info'
                            action_text = 'Xem'
                        elif 'POST' in message:
                            action_icon = 'fas fa-plus-circle text-success'
                            action_text = 'Tạo mới'
                        
                        activities.append({
                            'timestamp': timestamp,
                            'action_icon': action_icon,
                            'action_text': action_text,
                            'message': message,
                            'time_ago': get_time_ago(timestamp)
                        })
                    except:
                        continue
                        
    except Exception as e:
        # Fallback activities nếu không đọc được log
        activities = [
            {
                'timestamp': datetime.now(),
                'action_icon': 'fas fa-info-circle text-info',
                'action_text': 'Hệ thống',
                'message': 'Không thể đọc log file',
                'time_ago': 'Vừa xong'
            }
        ]
    
    # Sắp xếp theo thời gian mới nhất
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Tạo paginator với tối đa 24 hoạt động (4 trang x 6 hoạt động)
    paginator = Paginator(activities, per_page)
    
    try:
        page_obj = paginator.page(page)
        return {
            'activities': page_obj.object_list,
            'page_obj': page_obj,
            'has_other_pages': page_obj.has_other_pages(),
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'num_pages': paginator.num_pages,
            'current_page': page
        }
    except:
        # Fallback nếu phân trang lỗi
        return {
            'activities': activities[:per_page],
            'page_obj': None,
            'has_other_pages': False,
            'has_previous': False,
            'has_next': False,
            'previous_page_number': None,
            'next_page_number': None,
            'num_pages': 1,
            'current_page': 1
        }


def get_time_ago(timestamp):
    """Tính thời gian cách đây"""
    from datetime import datetime
    
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days} ngày trước"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} giờ trước"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} phút trước"
    else:
        return "Vừa xong"


@login_required(login_url='/auth/login/')
def category_list(request):
    """Danh sách categories với tìm kiếm và phân trang"""
    # Sử dụng mixin logic
    search_query = request.GET.get('search', '')
    categories = Category.objects.all().order_by('-created_at')
    
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(categories, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': categories.count(),
    }
    return render(request, 'admin/category_list.html', context)


@login_required(login_url='/auth/login/')
def category_create(request):
    """Tạo category mới"""
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category đã được tạo thành công!')
            return redirect('manage_category:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'admin/category_form.html', {
        'form': form,
        'title': 'Tạo Category Mới',
        'action': 'create'
    })


@login_required(login_url='/auth/login/')
def category_edit(request, pk):
    """Chỉnh sửa category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category đã được cập nhật thành công!')
            return redirect('manage_category:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'admin/category_form.html', {
        'form': form,
        'category': category,
        'title': 'Chỉnh sửa Category',
        'action': 'edit'
    })


@login_required(login_url='/auth/login/')
def category_delete(request, pk):
    """Xóa category"""
    if request.method != 'POST':
        return redirect('manage_category:category_list')
    
    category = get_object_or_404(Category, pk=pk)
    category_name = category.name
    category.delete()
    messages.success(request, f'Category "{category_name}" đã được xóa thành công!')
    return redirect('manage_category:category_list')


@login_required(login_url='/auth/login/')
def category_detail(request, pk):
    """Chi tiết category"""
    category = get_object_or_404(Category, pk=pk)
    products_count = category.category_products.count()  # Chỉ đếm số lượng products
    
    context = {
        'category': category,
        'products_count': products_count,
    }
    return render(request, 'admin/category_detail.html', context)


@login_required(login_url='/auth/login/')
def category_product_create(request, category_id):
    """Tạo product mới với category được chọn trước"""
    from apps.product.forms import ProductForm
    from apps.product.models import Product
    
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.save()
            messages.success(request, f'Product "{product.name}" đã được tạo thành công trong category "{category.name}"!')
            return redirect('manage_product:product_detail', pk=product.pk)
    else:
        form = ProductForm(initial={'category': category})
    
    return render(request, 'admin/product_form.html', {
        'form': form,
        'title': f'Tạo Product Mới trong Category "{category.name}"',
        'action': 'create',
        'category': category,
    })