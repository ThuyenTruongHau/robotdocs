/**
 * Category Real-time Search
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="search"]');
    if (!searchInput) return;
    
    // Template cho kết quả tìm kiếm category
    const categoryTemplate = (category) => `
        <div class="search-result-item p-3 border-bottom" 
             style="cursor: pointer; transition: background-color 0.2s;"
             onmouseover="this.style.backgroundColor='#f8f9fa'"
             onmouseout="this.style.backgroundColor='white'"
             onclick="selectCategory(${category.id}, '${category.name.replace(/'/g, "\\'")}')">
            <div class="d-flex align-items-center">
                <div class="me-3">
                    ${category.image ? 
                        `<img src="${category.image}" alt="${category.name}" 
                              style="width: 40px; height: 40px; object-fit: cover;" 
                              class="rounded">` :
                        `<div class="bg-light d-flex align-items-center justify-content-center rounded" 
                              style="width: 40px; height: 40px;">
                            <i class="fas fa-image text-muted"></i>
                         </div>`
                    }
                </div>
                <div class="flex-grow-1">
                    <div class="fw-bold text-primary">${category.name}</div>
                    <div class="text-muted small">
                        ${category.description ? truncateText(category.description, 60) : 'Không có mô tả'}
                    </div>
                    <div class="text-muted small mt-1">
                        <i class="fas fa-box me-1"></i>
                        ${category.product_count || 0} sản phẩm
                        <span class="ms-2">
                            <i class="fas fa-calendar me-1"></i>
                            ${formatDate(category.created_at)}
                        </span>
                    </div>
                </div>
                <div class="text-end">
                    <i class="fas fa-arrow-right text-muted"></i>
                </div>
            </div>
        </div>
    `;
    
    // Template khi không có kết quả
    const emptyTemplate = `
        <div class="p-4 text-center text-muted">
            <i class="fas fa-search fa-2x mb-3"></i>
            <div class="fw-bold">Không tìm thấy category nào</div>
            <div class="small">Thử tìm kiếm với từ khóa khác</div>
        </div>
    `;
    
    // Khởi tạo real-time search
    const search = new RealtimeSearch({
        searchInput: searchInput,
        apiUrl: '/api/categories/search/',
        minLength: 1,
        delay: 200,
        template: categoryTemplate,
        emptyTemplate: emptyTemplate
    });
    
    // Thêm style cho search input
    searchInput.style.position = 'relative';
    searchInput.style.zIndex = '999';
});

// Function để chọn category từ kết quả tìm kiếm
function selectCategory(categoryId, categoryName) {
    // Redirect đến trang chi tiết category
    window.location.href = `/manage/categories/${categoryId}/`;
}

// Function để tìm kiếm và submit form (cho tương thích ngược)
function searchCategories() {
    const searchInput = document.querySelector('input[name="search"]');
    const form = searchInput.closest('form');
    if (form) {
        form.submit();
    }
}
