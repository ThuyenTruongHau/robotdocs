// Brand Delete Functionality
document.addEventListener('DOMContentLoaded', function() {
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    const deleteForm = document.getElementById('deleteForm');
    const deleteTitle = document.getElementById('deleteTitle');
    const deleteMessage = document.getElementById('deleteMessage');
    
    // Xử lý tất cả nút xóa brand
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-btn') || e.target.closest('.delete-btn')) {
            const btn = e.target.classList.contains('delete-btn') ? e.target : e.target.closest('.delete-btn');
            
            const brandId = btn.dataset.brandId;
            const brandName = btn.dataset.brandName;
            const productsCount = parseInt(btn.dataset.productsCount || 0);
            
            // Cập nhật tiêu đề modal
            deleteTitle.textContent = `Xóa Brand "${brandName}"`;
            
            // Cập nhật nội dung modal dựa trên số lượng products
            if (productsCount > 0) {
                deleteMessage.innerHTML = `
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle"></i>
                        <strong>Cảnh báo:</strong> Brand này có <strong>${productsCount}</strong> product(s). 
                        Việc xóa brand có thể ảnh hưởng đến các product này.
                    </div>
                    <p>Bạn có chắc chắn muốn xóa brand "<strong>${brandName}</strong>" không?</p>
                `;
            } else {
                deleteMessage.innerHTML = `
                    <p>Bạn có chắc chắn muốn xóa brand "<strong>${brandName}</strong>" không?</p>
                    <p class="text-muted">Hành động này không thể hoàn tác.</p>
                `;
            }
            
            // Cập nhật action của form để trỏ đến URL xóa đúng
            const baseUrl = window.location.origin + '/manage/brands/';
            deleteForm.action = `${baseUrl}${brandId}/delete/`;
            
            // Hiển thị modal
            deleteModal.show();
        }
    });
    
    // Xử lý submit form xóa
    if (deleteForm) {
        deleteForm.addEventListener('submit', function(e) {
            // Disable submit button để tránh double-click
            const submitBtn = deleteForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang xóa...';
            }
        });
    }
    
    // Reset form khi modal đóng
    document.getElementById('deleteModal').addEventListener('hidden.bs.modal', function() {
        const submitBtn = deleteForm.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-trash"></i> Xóa';
        }
    });
});

// Utility function để escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}
