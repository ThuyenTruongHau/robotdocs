# apps/product/serializers.py
from rest_framework import serializers
from .models import Product, ProductImage
from apps.category.models import Category
from apps.brand.models import Brand

class CategoryInPorductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

class BrandInPorductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "description"]

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "image_url"]
    
    def get_image_url(self, obj):
        if obj.image:
            # Return relative URL, frontend will handle full URL construction
            return obj.image.url
        return None

    def update(self, instance, validated_data):
        if "image" in validated_data:
            new_image = validated_data.get("image")
            if new_image:  
                # Có ảnh mới => xóa ảnh cũ
                if instance.image:
                    instance.image.delete(save=False)
            else:
                # Client gửi null => giữ ảnh cũ
                validated_data.pop("image")

        return super().update(instance, validated_data)

class ProductSerializer(serializers.ModelSerializer):
    # Hiển thị thông tin category chi tiết
    category = CategoryInPorductSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand = BrandInPorductSerializer(read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    # Cho phép gán category bằng id khi tạo/sửa product
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True
    )

    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        source="brand",
        write_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "parameters",
            "category",
            "category_id",
            "category_name",
            "brand",
            "brand_id",
            "brand_name",
            "images",
            "created_at",
            "updated_at",
        ]

