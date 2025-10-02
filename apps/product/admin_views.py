from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, ProductImage
from .forms import ProductForm, ProductImageForm
from apps.category.models import Category
from apps.brand.models import Brand


@login_required(login_url='/auth/login/')
def product_list(request):
    """Danh sách products với tìm kiếm và phân trang"""
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    brand_filter = request.GET.get('brand', '')
    
    products = Product.objects.select_related('category', 'brand').all().order_by('-created_at')
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    if brand_filter:
        products = products.filter(brand_id=brand_filter)
    
    paginator = Paginator(products, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'brand_filter': brand_filter,
        'categories': categories,
        'brands': brands,
        'total_count': products.count(),
    }
    return render(request, 'admin/product_list.html', context)


@login_required(login_url='/auth/login/')
def product_create(request):
    """Tạo product mới"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product đã được tạo thành công!')
            return redirect('manage_product:product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'admin/product_form.html', {
        'form': form,
        'product': None,  # Truyền None cho trường hợp tạo mới
        'title': 'Tạo Product Mới',
        'action': 'create'
    })


@login_required(login_url='/auth/login/')
def product_edit(request, pk):
    """Chỉnh sửa product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product đã được cập nhật thành công!')
            return redirect('manage_product:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'admin/product_form.html', {
        'form': form,
        'product': product,
        'title': 'Chỉnh sửa Product',
        'action': 'edit'
    })


@login_required(login_url='/auth/login/')
def product_delete(request, pk):
    """Xóa product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" đã được xóa thành công!')
        
        # Redirect về trang trước đó hoặc product list
        referer = request.META.get('HTTP_REFERER')
        if referer and 'product_detail' in referer:
            # Nếu đến từ product detail, redirect về product list
            return redirect('manage_product:product_list')
        else:
            # Nếu đến từ product list, redirect về product list
            return redirect('manage_product:product_list')
    
    # Nếu không phải POST request, redirect về product list
    return redirect('manage_product:product_list')


@login_required(login_url='/auth/login/')
def product_detail(request, pk):
    """Chi tiết product"""
    product = get_object_or_404(Product.objects.select_related('category', 'brand'), pk=pk)
    images = product.images.all()
    
    context = {
        'product': product,
        'images': images,
        'images_count': images.count(),
    }
    return render(request, 'admin/product_detail.html', context)


@login_required(login_url='/auth/login/')
def product_image_add(request, product_pk):
    """Thêm hình ảnh cho product"""
    product = get_object_or_404(Product, pk=product_pk)
    
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.product = product
            image.save()
            messages.success(request, 'Hình ảnh đã được thêm thành công!')
            return redirect('manage_product:product_detail', pk=product.pk)
    else:
        form = ProductImageForm()
    
    return render(request, 'admin/product_image_form.html', {
        'form': form,
        'product': product,
        'title': 'Thêm Hình Ảnh'
    })


@login_required(login_url='/auth/login/')
def product_image_delete(request, pk):
    """Xóa hình ảnh của product"""
    image = get_object_or_404(ProductImage, pk=pk)
    product = image.product
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Hình ảnh đã được xóa thành công!')
        return redirect('manage_product:product_detail', pk=product.pk)
    
    # Nếu không phải POST request, redirect về product detail
    return redirect('manage_product:product_detail', pk=product.pk)
