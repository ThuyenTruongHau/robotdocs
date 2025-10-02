from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Brand
from .forms import BrandForm
from apps.core.mixins import AdminListMixin

@login_required(login_url='/auth/login/')
def brand_list(request):
    """Danh sách brands với tìm kiếm và phân trang"""
    # Sử dụng mixin logic
    search_query = request.GET.get('search', '')
    brands = Brand.objects.all().order_by('-created_at')
    
    if search_query:
        brands = brands.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(brands, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': brands.count(),
    }
    return render(request, 'admin/brand_list.html', context)


@login_required(login_url='/auth/login/')
def brand_create(request):
    """Tạo brand mới"""
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand đã được tạo thành công!')
            return redirect('manage_brand:brand_list')
    else:
        form = BrandForm()
    
    return render(request, 'admin/brand_form.html', {
        'form': form,
        'title': 'Tạo Brand Mới',
        'action': 'create'
    })


@login_required(login_url='/auth/login/')
def brand_edit(request, pk):
    """Chỉnh sửa brand"""
    brand = get_object_or_404(Brand, pk=pk)
    
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand đã được cập nhật thành công!')
            return redirect('manage_brand:brand_list')
    else:
        form = BrandForm(instance=brand)
    
    return render(request, 'admin/brand_form.html', {
        'form': form,
        'brand': brand,
        'title': 'Chỉnh sửa Brand',
        'action': 'edit'
    })


@login_required(login_url='/auth/login/')
def brand_delete(request, pk):
    """Xóa brand"""
    if request.method != 'POST':
        return redirect('manage_brand:brand_list')
    
    brand = get_object_or_404(Brand, pk=pk)
    brand_name = brand.name
    brand.delete()
    messages.success(request, f'Brand "{brand_name}" đã được xóa thành công!')
    return redirect('manage_brand:brand_list')


@login_required(login_url='/auth/login/')
def brand_detail(request, pk):
    """Chi tiết brand"""
    brand = get_object_or_404(Brand, pk=pk)
    products_count = brand.brand_products.count()  # Chỉ đếm số lượng products
    
    context = {
        'brand': brand,
        'products_count': products_count,
    }
    return render(request, 'admin/brand_detail.html', context)


@login_required(login_url='/auth/login/')
def brand_product_create(request, brand_id):
    """Tạo product mới với brand được chọn trước"""
    from apps.product.forms import ProductForm
    from apps.product.models import Product
    
    brand = get_object_or_404(Brand, pk=brand_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.brand = brand
            product.save()
            messages.success(request, f'Product "{product.name}" đã được tạo thành công trong brand "{brand.name}"!')
            return redirect('manage_product:product_detail', pk=product.pk)
    else:
        form = ProductForm(initial={'brand': brand})
    
    return render(request, 'admin/product_form.html', {
        'form': form,
        'title': f'Tạo Product Mới trong Brand "{brand.name}"',
        'action': 'create',
        'brand': brand,
    })