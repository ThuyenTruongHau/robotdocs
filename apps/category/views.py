from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD cho Category:
    - list (GET /categories/)
    - retrieve (GET /categories/{id}/)
    - create (POST /categories/)
    - update (PUT /categories/{id}/)
    - partial_update (PATCH /categories/{id}/)
    - destroy (DELETE /categories/{id}/)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Tìm kiếm real-time categories"""
        query = request.GET.get('q', '')
        if not query:
            return Response({'results': []})
        
        categories = Category.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        ).order_by('-created_at')[:5]  # Giới hạn 5 kết quả
        
        serializer = self.get_serializer(categories, many=True)
        return Response({
            'results': serializer.data,
            'count': categories.count()
        })
