from django.db import models
import os, uuid

def product_image_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"category/{uuid.uuid4().hex}{ext}"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)   # lưu thời điểm tạo
    updated_at = models.DateTimeField(auto_now=True)       # lưu thời điểm cập nhật

    class Meta:
        db_table = "category"          # tên bảng trong DB
        ordering = ["-created_at"]     # mặc định sắp xếp theo ngày tạo mới nhất
        verbose_name = "Category"      # tên hiển thị trong admin
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name 
    
