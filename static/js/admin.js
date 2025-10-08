// Funções para gerenciar modais

function openCreateModal() {
    document.getElementById('createModal').classList.add('show');
}

function closeCreateModal() {
    document.getElementById('createModal').classList.remove('show');
}

function openEditModal(userId, username, role) {
    const modal = document.getElementById('editModal');
    const form = document.getElementById('editForm');
    
    // Configurar action do formulário
    form.action = `/admin/edit_user/${userId}`;
    
    // Preencher campos
    document.getElementById('edit_username').value = username;
    document.getElementById('edit_password').value = '';
    document.getElementById('edit_role').value = role;
    
    modal.classList.add('show');
}

function closeEditModal() {
    document.getElementById('editModal').classList.remove('show');
}

function deleteUser(userId, username) {
    if (confirm(`Tem certeza que deseja deletar o usuário "${username}"?`)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin/delete_user/${userId}`;
        document.body.appendChild(form);
        form.submit();
    }
}

// Função para alternar submenus
function toggleMenu(element) {
    const submenu = element.nextElementSibling;
    const isActive = submenu.classList.contains('active');
    
    // Fecha todos os submenus abertos
    document.querySelectorAll('.submenu.active').forEach(openSubmenu => {
        if (openSubmenu !== submenu) {
            openSubmenu.classList.remove('active');
            openSubmenu.previousElementSibling.classList.remove('active');
        }
    });

    // Abre ou fecha o submenu clicado
    submenu.classList.toggle('active');
    element.classList.toggle('active');
}

// Fechar modais ao clicar fora
window.onclick = function(event) {
    const createModal = document.getElementById('createModal');
    const editModal = document.getElementById('editModal');
    
    if (event.target == createModal) {
        closeCreateModal();
    }
    if (event.target == editModal) {
        closeEditModal();
    }
}

// Auto-hide alerts
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
});
