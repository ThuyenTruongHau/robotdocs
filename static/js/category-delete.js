/**
 * Category Delete Confirmation Modal
 * Tái sử dụng cho cả category_list và category_detail
 */
document.addEventListener('DOMContentLoaded', function() {
    // Event delegation cho tất cả nút xóa
    document.addEventListener('click', function(e) {
        if (e.target.closest('.delete-btn')) {
            const btn = e.target.closest('.delete-btn');
            const categoryId = btn.getAttribute('data-category-id');
            const categoryName = btn.getAttribute('data-category-name');
            const productsCount = parseInt(btn.getAttribute('data-products-count'));
            
            confirmDelete(categoryId, categoryName, productsCount);
        }
    });
});

function confirmDelete(categoryId, categoryName, productsCount) {
    // Cập nhật thông tin trong modal
    document.getElementById('categoryName').textContent = categoryName;
    
    // Hiển thị cảnh báo nếu có products
    const productsWarning = document.getElementById('productsWarning');
    if (productsCount > 0) {
        document.getElementById('productsCount').textContent = productsCount;
        productsWarning.style.display = 'block';
    } else {
        productsWarning.style.display = 'none';
    }
    
    // Cập nhật action của form
    document.getElementById('deleteForm').action = `/manage/categories/${categoryId}/delete/`;
    
    // Hiển thị modal
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}
