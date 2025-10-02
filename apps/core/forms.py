from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile, SystemSettings

User = get_user_model()


class UserForm(forms.ModelForm):
    """Form cho User"""
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập mật khẩu mới...'
        })
    )
    password_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Xác nhận mật khẩu...'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập username...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập email...'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên...'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập họ...'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        # Lấy action từ kwargs để phân biệt create/edit
        self.action = kwargs.pop('action', 'edit')
        super().__init__(*args, **kwargs)
        
        self.fields['username'].required = True
        self.fields['email'].required = True
        
        # Phân biệt logic cho create và edit
        if self.action == 'create':
            # Tạo mới: bắt buộc password
            self.fields['password'].required = True
            self.fields['password_confirm'].required = True
            self.fields['password'].help_text = "Nhập mật khẩu cho user mới"
            self.fields['password'].widget.attrs['placeholder'] = 'Nhập mật khẩu...'
            self.fields['password_confirm'].widget.attrs['placeholder'] = 'Xác nhận mật khẩu...'
        else:
            # Chỉnh sửa: password là tùy chọn
            self.fields['password'].required = False
            self.fields['password_confirm'].required = False
            self.fields['password'].help_text = "Để trống nếu không muốn thay đổi mật khẩu"
            self.fields['password'].widget.attrs['placeholder'] = 'Nhập mật khẩu mới...'
            self.fields['password_confirm'].widget.attrs['placeholder'] = 'Xác nhận mật khẩu mới...'
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Kiểm tra độ dài
            if len(username) < 3:
                raise forms.ValidationError("Username phải có ít nhất 3 ký tự")
            
            if len(username) > 150:
                raise forms.ValidationError("Username không được quá 150 ký tự")
        
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Kiểm tra password
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        # Logic khác nhau cho create và edit
        if self.action == 'create':
            # Tạo mới: bắt buộc phải có password
            if not password:
                raise forms.ValidationError("Mật khẩu là bắt buộc khi tạo user mới!")
            if not password_confirm:
                raise forms.ValidationError("Xác nhận mật khẩu là bắt buộc khi tạo user mới!")
            if password != password_confirm:
                raise forms.ValidationError("Mật khẩu xác nhận không khớp!")
        else:
            # Chỉnh sửa: password là tùy chọn, nhưng nếu nhập thì phải khớp
            if password or password_confirm:
                if password != password_confirm:
                    raise forms.ValidationError("Mật khẩu xác nhận không khớp!")
                if password and len(password) < 6:
                    raise forms.ValidationError("Mật khẩu phải có ít nhất 6 ký tự!")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        # Chỉ set password nếu có password mới
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Form cho UserProfile"""
    
    class Meta:
        model = UserProfile
        fields = ['role', 'department']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].required = True
        self.fields['department'].required = True


class SystemSettingsForm(forms.Form):
    """Form cho cài đặt hệ thống"""
    logo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text="Upload logo mới cho hệ thống"
    )
    
    site_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tên hệ thống...'
        }),
        help_text="Tên hiển thị của hệ thống"
    )
    
    site_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Mô tả hệ thống...'
        }),
        help_text="Mô tả ngắn về hệ thống"
    )
    
    primary_color = forms.CharField(
        max_length=7,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'color',
            'value': '#2563eb'
        }),
        help_text="Màu chủ đạo của giao diện"
    )
    
    secondary_color = forms.CharField(
        max_length=7,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'color',
            'value': '#64748b'
        }),
        help_text="Màu phụ của giao diện"
    )
