"""
Mixin classes for common admin functionality
"""
from django.core.paginator import Paginator
from django.db.models import Q


class AdminListMixin:
    """
    Mixin cho các view list admin với tìm kiếm và phân trang
    """
    model = None
    search_fields = []
    filter_field = None
    filter_choices = []
    per_page = 10
    order_by = '-created_at'
    
    def get_queryset(self):
        """Lấy queryset cơ bản"""
        return self.model.objects.all().order_by(self.order_by)
    
    def apply_search(self, queryset, search_query):
        """Áp dụng tìm kiếm"""
        if not search_query or not self.search_fields:
            return queryset
            
        query = Q()
        for field in self.search_fields:
            query |= Q(**{f"{field}__icontains": search_query})
        
        return queryset.filter(query)
    
    def apply_filter(self, queryset, filter_value):
        """Áp dụng filter"""
        if not filter_value or not self.filter_field:
            return queryset
            
        return queryset.filter(**{self.filter_field: filter_value})
    
    def get_context_data(self, **kwargs):
        """Lấy context data cho template"""
        search_query = self.request.GET.get('search', '')
        filter_value = self.request.GET.get(self.filter_field or 'filter', '')
        
        # Lấy queryset
        queryset = self.get_queryset()
        queryset = self.apply_search(queryset, search_query)
        queryset = self.apply_filter(queryset, filter_value)
        
        # Phân trang
        paginator = Paginator(queryset, self.per_page)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Context
        context = {
            'page_obj': page_obj,
            'search_query': search_query,
            'total_count': queryset.count(),
        }
        
        # Thêm filter context nếu có
        if self.filter_field:
            context.update({
                'filter_options': self.filter_choices,
                'filter_name': self.filter_field,
                'current_filter': filter_value,
            })
        
        context.update(kwargs)
        return context


class AdminFormMixin:
    """
    Mixin cho các view form admin
    """
    success_message = "Thao tác thành công!"
    success_url = None
    
    def get_success_url(self):
        """Lấy URL redirect sau khi thành công"""
        if self.success_url:
            return self.success_url
        return super().get_success_url()
    
    def form_valid(self, form):
        """Xử lý khi form hợp lệ"""
        response = super().form_valid(form)
        if hasattr(self, 'request') and hasattr(self.request, '_messages'):
            from django.contrib import messages
            messages.success(self.request, self.success_message)
        return response
