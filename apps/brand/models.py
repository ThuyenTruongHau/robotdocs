from django.db import models
import os, uuid

# Create your models here.
def brand_image_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"brands/{uuid.uuid4().hex}{ext}"

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=brand_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "brand"          # tên bảng trong DB
        ordering = ["-created_at"]     # mặc định sắp xếp theo ngày tạo mới nhất
        verbose_name = "Brand"         # tên hiển thị trong admin
        verbose_name_plural = "Brands"

    def __str__(self): 
        return self.name