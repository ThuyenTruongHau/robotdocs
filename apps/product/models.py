# apps/product/models.py
from django.db import models
from apps.category.models import Category
from apps.brand.models import Brand
import os, uuid


def product_image_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"products/{uuid.uuid4().hex}{ext}"

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Product Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    parameters = models.JSONField(blank=True, null=True, verbose_name="Parameters")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,   
        related_name="category_products"   
    )
    brand = models.ForeignKey(
        Brand, 
        on_delete=models.CASCADE,   
        related_name="brand_products",
        default=1    
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image of {self.product.name}"
