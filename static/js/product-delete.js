/**
 * Product Delete Confirmation Modal
 * Tái sử dụng cho cả product_list và product_detail
 */
document.addEventListener('DOMContentLoaded', function() {
    // Event delegation cho tất cả nút xóa product
    document.addEventListener('click', function(e) {
        if (e.target.closest('.product-delete-btn')) {
            const btn = e.target.closest('.product-delete-btn');
            const productId = btn.getAttribute('data-product-id');
            const productName = btn.getAttribute('data-product-name');
            
            confirmProductDelete(productId, productName);
        }
    });
});

function confirmProductDelete(productId, productName) {
    // Cập nhật tên product
    document.getElementById('productName').textContent = productName;
    
    // Cập nhật action của form
    document.getElementById('productDeleteForm').action = `/manage/products/${productId}/delete/`;
    
    // Hiển thị modal
    const modal = new bootstrap.Modal(document.getElementById('productDeleteModal'));
    modal.show();
}
