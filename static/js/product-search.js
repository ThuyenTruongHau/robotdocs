/**
 * Product Real-time Search
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="search"]');
    if (!searchInput) return;
    
    // Template cho kết quả tìm kiếm product
    const productTemplate = (product) => `
        <div class="search-result-item p-3 border-bottom" 
             style="cursor: pointer; transition: background-color 0.2s;"
             onmouseover="this.style.backgroundColor='#f8f9fa'"
             onmouseout="this.style.backgroundColor='white'"
             onclick="selectProduct(${product.id}, '${product.name.replace(/'/g, "\\'")}')">
            <div class="d-flex align-items-center">
                <div class="me-3">
                    ${product.images && product.images.length > 0 ? 
                        `<img src="${product.images[0].image}" alt="${product.name}" 
                              style="width: 40px; height: 40px; object-fit: cover;" 
                              class="rounded">` :
                        `<div class="bg-light d-flex align-items-center justify-content-center rounded" 
                              style="width: 40px; height: 40px;">
                            <i class="fas fa-image text-muted"></i>
                         </div>`
                    }
                </div>
                <div class="flex-grow-1">
                    <div class="fw-bold text-primary">${product.name}</div>
                    <div class="text-muted small">
                        ${product.description ? truncateText(product.description, 60) : 'Không có mô tả'}
                    </div>
                    <div class="text-muted small mt-1">
                        <span class="badge bg-info me-2">${product.category_name}</span>
                        <span>
                            <i class="fas fa-calendar me-1"></i>
                            ${formatDate(product.created_at)}
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
            <div class="fw-bold">Không tìm thấy sản phẩm nào</div>
            <div class="small">Thử tìm kiếm với từ khóa khác hoặc chọn category khác</div>
        </div>
    `;
    
    // Khởi tạo real-time search
    const search = new RealtimeSearch({
        searchInput: searchInput,
        apiUrl: '/api/products/search/',
        minLength: 1,
        delay: 200,
        template: productTemplate,
        emptyTemplate: emptyTemplate
    });
    
    // Thêm style cho search input
    searchInput.style.position = 'relative';
    searchInput.style.zIndex = '999';
    
    // Xử lý filter category
    const categorySelect = document.querySelector('select[name="category"]');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            const categoryId = this.value;
            const currentQuery = searchInput.value.trim();
            
            if (currentQuery.length >= 1) {
                // Cập nhật URL search với category filter
                search.apiUrl = categoryId ? 
                    `/api/products/search/?category=${categoryId}` : 
                    '/api/products/search/';
                
                // Thực hiện search lại
                if (search.timeout) {
                    clearTimeout(search.timeout);
                }
                search.timeout = setTimeout(() => {
                    search.performSearch(currentQuery);
                }, 100);
            }
        });
    }
});

// Function để chọn product từ kết quả tìm kiếm
function selectProduct(productId, productName) {
    // Redirect đến trang chi tiết product
    window.location.href = `/manage/products/${productId}/`;
}

// Function để tìm kiếm và submit form (cho tương thích ngược)
function searchProducts() {
    const searchInput = document.querySelector('input[name="search"]');
    const form = searchInput.closest('form');
    if (form) {
        form.submit();
    }
}
