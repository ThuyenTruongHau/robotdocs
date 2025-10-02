# apps/product/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    API cho Product (CRUD).
    Swagger sẽ tự động sinh docs từ serializer + viewset.
    """
    queryset = Product.objects.select_related('category', 'brand').prefetch_related('images').all().order_by("-created_at")
    serializer_class = ProductSerializer
    #permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Tìm kiếm real-time products"""
        query = request.GET.get('q', '')
        category_id = request.GET.get('category', '')
        
        products = Product.objects.select_related('category', 'brand').prefetch_related('images').all()
        
        if query:
            products = products.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            )
        
        if category_id:
            products = products.filter(category_id=category_id)
        
        products = products.order_by('-created_at')[:5]  # Giới hạn 5 kết quả
        
        serializer = self.get_serializer(products, many=True)
        return Response({
            'results': serializer.data,
            'count': products.count()
        })

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    #permission_classes = [IsAuthenticated]
