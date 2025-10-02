from django import forms
from django.core.exceptions import ValidationError
import json
from .models import Product, ProductImage
from apps.category.models import Category
from apps.brand.models import Brand


class ProductForm(forms.ModelForm):
    """Form cho Product"""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'parameters', 'category', 'brand']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên sản phẩm...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Nhập mô tả sản phẩm...'
            }),
            'parameters': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Nhập thông số kỹ thuật (JSON format)...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'brand': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['category'].required = True
        self.fields['brand'].required = True
        self.fields['description'].required = False
        self.fields['parameters'].required = False
        
        # Populate category choices
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Chọn category..."
        
        # Populate brand choices
        self.fields['brand'].queryset = Brand.objects.all()
        self.fields['brand'].empty_label = "Chọn brand..."
    
    def clean_parameters(self):
        """Validate parameters field"""
        parameters = self.cleaned_data.get('parameters')
        
        # If parameters is empty or None, that's fine
        if not parameters:
            return parameters
        
        # If parameters is a string, try to parse it as JSON
        if isinstance(parameters, str):
            try:
                parameters = json.loads(parameters)
            except json.JSONDecodeError:
                raise ValidationError('Định dạng JSON không hợp lệ cho thông số kỹ thuật.')
        
        # Validate the structure of parameters
        if isinstance(parameters, dict):
            errors = []
            
            for section_name, section_data in parameters.items():
                # Check if section name is empty
                if not section_name or not section_name.strip():
                    errors.append('Tên tiêu đề không được để trống.')
                    continue
                
                # Check if section data is a dictionary
                if not isinstance(section_data, dict):
                    errors.append(f'Dữ liệu tiêu đề "{section_name}" không hợp lệ.')
                    continue
                
                # Check if section has parameters
                if not section_data:
                    errors.append(f'Tiêu đề "{section_name}" cần có ít nhất 1 thông số.')
                    continue
                
                # Check each parameter in the section
                for param_name, param_value in section_data.items():
                    # Check if parameter name is empty
                    if not param_name or not param_name.strip():
                        errors.append(f'Tiêu đề "{section_name}" có thông số thiếu tên.')
                        continue
                    
                    # Check if parameter value is empty
                    if not param_value or not param_value.strip():
                        errors.append(f'Thông số "{param_name}" trong tiêu đề "{section_name}" thiếu giá trị.')
                        continue
            
            # If there are validation errors, raise them
            if errors:
                raise ValidationError(errors)
        
        return parameters


class ProductImageForm(forms.ModelForm):
    """Form cho ProductImage"""
    
    class Meta:
        model = ProductImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True
