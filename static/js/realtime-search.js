/**
 * Real-time Search Functionality
 * Hỗ trợ tìm kiếm real-time cho categories và products
 */

class RealtimeSearch {
    constructor(options) {
        this.searchInput = options.searchInput;
        this.resultsContainer = options.resultsContainer;
        this.apiUrl = options.apiUrl;
        this.minLength = options.minLength || 2;
        this.delay = options.delay || 300;
        this.template = options.template;
        this.emptyTemplate = options.emptyTemplate;
        this.onSelect = options.onSelect || null;
        
        this.timeout = null;
        this.isVisible = false;
        
        this.init();
    }
    
    init() {
        // Tạo container cho kết quả tìm kiếm
        this.createResultsContainer();
        
        // Bind events
        this.searchInput.addEventListener('input', this.handleInput.bind(this));
        this.searchInput.addEventListener('focus', this.handleFocus.bind(this));
        this.searchInput.addEventListener('blur', this.handleBlur.bind(this));
        
        // Click outside để đóng dropdown
        document.addEventListener('click', this.handleOutsideClick.bind(this));
        
        // Escape key để đóng dropdown
        document.addEventListener('keydown', this.handleKeydown.bind(this));
    }
    
    createResultsContainer() {
        if (!this.resultsContainer) {
            this.resultsContainer = document.createElement('div');
            this.resultsContainer.className = 'realtime-search-results';
            this.resultsContainer.style.cssText = `
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: white;
                border: 1px solid #dee2e6;
                border-top: none;
                border-radius: 0 0 0.375rem 0.375rem;
                box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
                max-height: 300px;
                overflow-y: auto;
                z-index: 1000;
                display: none;
            `;
            
            // Insert after search input
            this.searchInput.parentNode.insertBefore(this.resultsContainer, this.searchInput.nextSibling);
        }
    }
    
    handleInput(e) {
        const query = e.target.value.trim();
        
        // Clear previous timeout
        if (this.timeout) {
            clearTimeout(this.timeout);
        }
        
        // Hide results if query is too short
        if (query.length < this.minLength) {
            this.hideResults();
            return;
        }
        
        // Debounce search
        this.timeout = setTimeout(() => {
            this.performSearch(query);
        }, this.delay);
    }
    
    handleFocus(e) {
        const query = e.target.value.trim();
        if (query.length >= this.minLength) {
            this.showResults();
        }
    }
    
    handleBlur(e) {
        // Delay để cho phép click vào kết quả
        setTimeout(() => {
            this.hideResults();
        }, 200);
    }
    
    handleOutsideClick(e) {
        if (!this.searchInput.contains(e.target) && !this.resultsContainer.contains(e.target)) {
            this.hideResults();
        }
    }
    
    handleKeydown(e) {
        if (e.key === 'Escape') {
            this.hideResults();
            this.searchInput.blur();
        }
    }
    
    async performSearch(query) {
        try {
            this.showLoading();
            
            const url = `${this.apiUrl}?q=${encodeURIComponent(query)}`;
            const response = await fetch(url);
            const data = await response.json();
            
            this.displayResults(data.results || []);
        } catch (error) {
            console.error('Search error:', error);
            this.showError();
        }
    }
    
    showLoading() {
        this.resultsContainer.innerHTML = `
            <div class="p-3 text-center text-muted">
                <i class="fas fa-spinner fa-spin me-2"></i>
                Đang tìm kiếm...
            </div>
        `;
        this.showResults();
    }
    
    showError() {
        this.resultsContainer.innerHTML = `
            <div class="p-3 text-center text-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Lỗi tìm kiếm. Vui lòng thử lại.
            </div>
        `;
        this.showResults();
    }
    
    displayResults(results) {
        if (results.length === 0) {
            this.resultsContainer.innerHTML = this.emptyTemplate || `
                <div class="p-3 text-center text-muted">
                    <i class="fas fa-search me-2"></i>
                    Không tìm thấy kết quả nào
                </div>
            `;
        } else {
            this.resultsContainer.innerHTML = results.map(item => this.template(item)).join('');
        }
        this.showResults();
    }
    
    showResults() {
        this.resultsContainer.style.display = 'block';
        this.isVisible = true;
    }
    
    hideResults() {
        this.resultsContainer.style.display = 'none';
        this.isVisible = false;
    }
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function truncateText(text, maxLength = 50) {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

// Export for use in other files
window.RealtimeSearch = RealtimeSearch;
window.formatDate = formatDate;
window.truncateText = truncateText;
