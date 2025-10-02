from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Brand
from .serializers import BrandSerializer

class BrandViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD cho Brand:
    - list (GET /brands/)
    - retrieve (GET /brands/{id}/)
    - create (POST /brands/)
    - update (PUT /brands/{id}/)
    - partial_update (PATCH /brands/{id}/)
    - destroy (DELETE /brands/{id}/)
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Tìm kiếm real-time brands"""
        query = request.GET.get('q', '')
        if not query:
            return Response({'results': []})
        
        brands = Brand.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        ).order_by('-created_at')[:5]  # Giới hạn 5 kết quả
        
        serializer = self.get_serializer(brands, many=True)
        return Response({
            'results': serializer.data,
            'count': brands.count()
        })
 