// Автоматическая отправка формы фильтрации при изменении
document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.querySelector('.filter-form');
    
    if (filterForm) {
        // Добавляем обработчики на все поля формы
        const filterInputs = filterForm.querySelectorAll('select, input[type="date"]');
        
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                // Небольшая задержка для текстовых полей
                if (this.type === 'text') {
                    clearTimeout(this.searchTimeout);
                    this.searchTimeout = setTimeout(() => {
                        filterForm.submit();
                    }, 500);
                } else {
                    filterForm.submit();
                }
            });
        });
        
        // Обработка текстового поля с задержкой
        const clientInput = filterForm.querySelector('input[name="client"]');
        if (clientInput) {
            clientInput.addEventListener('input', function() {
                clearTimeout(this.searchTimeout);
                this.searchTimeout = setTimeout(() => {
                    filterForm.submit();
                }, 800);
            });
        }
    }
    
    // Подтверждение удаления (если будет добавлено)
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить этот заказ?')) {
                e.preventDefault();
            }
        });
    });
    
    // Анимация для статусов
    const statusElements = document.querySelectorAll('.status');
    statusElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
});

// Функция для экспорта данных в CSV (опционально)
function exportToCSV() {
    const table = document.querySelector('.orders-table');
    const rows = Array.from(table.rows);
    
    const csvContent = rows.map(row => {
        const cols = Array.from(row.cells);
        return cols.map(col => `"${col.textContent.trim()}"`).join(',');
    }).join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', 'orders.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}