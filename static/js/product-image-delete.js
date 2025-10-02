/**
 * Product Image Delete Confirmation Modal
 * Tái sử dụng cho product_detail và product_image_form
 */
document.addEventListener('DOMContentLoaded', function() {
    // Event delegation cho tất cả nút xóa hình ảnh
    document.addEventListener('click', function(e) {
        if (e.target.closest('.product-image-delete-btn')) {
            const btn = e.target.closest('.product-image-delete-btn');
            const imageId = btn.getAttribute('data-image-id');
            const imageUrl = btn.getAttribute('data-image-url');
            const productName = btn.getAttribute('data-product-name');
            const uploadedAt = btn.getAttribute('data-uploaded-at');
            
            confirmImageDelete(imageId, imageUrl, productName, uploadedAt);
        }
    });
});

function confirmImageDelete(imageId, imageUrl, productName, uploadedAt) {
    // Cập nhật hình ảnh preview
    const imagePreview = document.getElementById('imagePreview');
    if (imagePreview) {
        imagePreview.src = imageUrl;
        imagePreview.alt = productName;
    }
    
    // Cập nhật thông tin hình ảnh
    const imageInfo = document.getElementById('imageInfo');
    if (imageInfo) {
        imageInfo.textContent = `Product: ${productName} | Ngày tải lên: ${uploadedAt}`;
    }
    
    // Cập nhật action của form
    const deleteForm = document.getElementById('productImageDeleteForm');
    if (deleteForm) {
        deleteForm.action = `/manage/images/${imageId}/delete/`;
    }
    
    // Hiển thị modal
    const modalElement = document.getElementById('productImageDeleteModal');
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}
