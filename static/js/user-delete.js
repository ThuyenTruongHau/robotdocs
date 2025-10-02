/**
 * User Delete Confirmation Modal
 * Tái sử dụng cho cả user_list và user_detail
 */
document.addEventListener('DOMContentLoaded', function() {
    // Event delegation cho tất cả nút xóa user
    document.addEventListener('click', function(e) {
        if (e.target.closest('.user-delete-btn')) {
            const btn = e.target.closest('.user-delete-btn');
            const userId = btn.getAttribute('data-user-id');
            const userName = btn.getAttribute('data-user-name');
            
            confirmUserDelete(userId, userName);
        }
    });
});

function confirmUserDelete(userId, userName) {
    // Cập nhật thông tin trong modal
    document.getElementById('userName').textContent = userName;
    
    // Cập nhật action của form
    document.getElementById('userDeleteForm').action = `/manage/users/${userId}/delete/`;
    
    // Hiển thị modal
    const modal = new bootstrap.Modal(document.getElementById('userDeleteModal'));
    modal.show();
}
