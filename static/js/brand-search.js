/**
 * Brand Real-time Search
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="search"]');
    if (!searchInput) return;
    
    // Template cho kết quả tìm kiếm brand
    const brandTemplate = (brand) => `
        <div class="search-result-item p-3 border-bottom" 
             style="cursor: pointer; transition: background-color 0.2s;"
             onmouseover="this.style.backgroundColor='#f8f9fa'"
             onmouseout="this.style.backgroundColor='white'"
             onclick="selectBrand(${brand.id}, '${brand.name.replace(/'/g, "\\'")}')">
            <div class="d-flex align-items-center">
                <div class="me-3">
                    ${brand.image ? 
                        `<img src="${brand.image}" alt="${brand.name}" 
                              style="width: 40px; height: 40px; object-fit: cover;" 
                              class="rounded">` :
                        `<div class="bg-light d-flex align-items-center justify-content-center rounded" 
                              style="width: 40px; height: 40px;">
                            <i class="fas fa-image text-muted"></i>
                         </div>`
                    }
                </div>
                <div class="flex-grow-1">
                    <div class="fw-bold text-success">${brand.name}</div>
                    <div class="text-muted small">
                        ${brand.description ? truncateText(brand.description, 60) : 'Không có mô tả'}
                    </div>
                    <div class="text-muted small mt-1">
                        <i class="fas fa-box me-1"></i>
                        ${brand.product_count || 0} sản phẩm
                        <span class="ms-2">
                            <i class="fas fa-calendar me-1"></i>
                            ${formatDate(brand.created_at)}
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
            <div class="fw-bold">Không tìm thấy brand nào</div>
            <div class="small">Thử tìm kiếm với từ khóa khác</div>
        </div>
    `;
    
    // Khởi tạo real-time search
    const search = new RealtimeSearch({
        searchInput: searchInput,
        apiUrl: '/api/brands/search/',
        minLength: 1,
        delay: 200,
        template: brandTemplate,
        emptyTemplate: emptyTemplate
    });
    
    // Thêm style cho search input
    searchInput.style.position = 'relative';
    searchInput.style.zIndex = '999';
});

// Function để chọn brand từ kết quả tìm kiếm
function selectBrand(brandId, brandName) {
    // Redirect đến trang chi tiết brand
    window.location.href = `/manage/brands/${brandId}/`;
}

// Function để tìm kiếm và submit form (cho tương thích ngược)
function searchBrands() {
    const searchInput = document.querySelector('input[name="search"]');
    const form = searchInput.closest('form');
    if (form) {
        form.submit();
    }
}
