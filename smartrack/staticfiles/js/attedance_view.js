document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('#searchInput');
    const dateFilter = document.querySelector('#dateFilter');
    const sortableHeaders = document.querySelectorAll('.sortable');
    const tbody = document.querySelector('.attendance-table tbody');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    const pageNumbers = document.querySelector('.page-numbers');
    
    let currentPage = 1;
    const rowsPerPage = 10;
    
    // Sorting functionality
    sortableHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.sort;
            const currentOrder = header.dataset.order || 'asc';
            const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
            
            // Update sort icons
            sortableHeaders.forEach(h => {
                h.querySelector('i').className = 'fas fa-sort';
                h.dataset.order = '';
            });
            
            header.dataset.order = newOrder;
            header.querySelector('i').className = `fas fa-sort-${newOrder === 'asc' ? 'up' : 'down'}`;
            
            sortTable(column, newOrder);
        });
    });
    
    // Search functionality
    searchInput.addEventListener('input', filterTable);
    dateFilter.addEventListener('change', filterTable);
    
    function filterTable() {
        const searchTerm = searchInput.value.toLowerCase();
        const filterValue = dateFilter.value;
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        rows.forEach(row => {
            const name = row.cells[0].textContent.toLowerCase();
            const date = row.cells[1].textContent;
            
            const matchesSearch = name.includes(searchTerm);
            const matchesDate = filterDate(date, filterValue);
            
            row.style.display = matchesSearch && matchesDate ? '' : 'none';
        });
        
        updatePagination();
    }
    
    function filterDate(date, filter) {
        if (filter === 'all') return true;
        const rowDate = new Date(date);
        const today = new Date();
        
        switch(filter) {
            case 'today':
                return isSameDay(rowDate, today);
            case 'week':
                return isWithinDays(rowDate, today, 7);
            case 'month':
                return isWithinDays(rowDate, today, 30);
            default:
                return true;
        }
    }
    
    function sortTable(column, order) {
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const sortedRows = rows.sort((a, b) => {
            const aValue = a.cells[getColumnIndex(column)].textContent;
            const bValue = b.cells[getColumnIndex(column)].textContent;
            
            return order === 'asc' ? 
                aValue.localeCompare(bValue) : 
                bValue.localeCompare(aValue);
        });
        
        tbody.innerHTML = '';
        sortedRows.forEach(row => tbody.appendChild(row));
        updatePagination();
    }
    
    // Pagination
    function updatePagination() {
        const visibleRows = Array.from(tbody.querySelectorAll('tr'))
            .filter(row => row.style.display !== 'none');
        const totalPages = Math.ceil(visibleRows.length / rowsPerPage);
        
        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = currentPage === totalPages;
        
        // Update page numbers
        pageNumbers.innerHTML = '';
        for (let i = 1; i <= totalPages; i++) {
            const span = document.createElement('span');
            span.textContent = i;
            span.className = i === currentPage ? 'active' : '';
            span.addEventListener('click', () => goToPage(i));
            pageNumbers.appendChild(span);
        }
        
        // Show current page rows
        visibleRows.forEach((row, index) => {
            row.style.display = 
                index >= (currentPage - 1) * rowsPerPage && 
                index < currentPage * rowsPerPage ? '' : 'none';
        });
    }
    
    prevBtn.addEventListener('click', () => {
        if (currentPage > 1) goToPage(currentPage - 1);
    });
    
    nextBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(
            tbody.querySelectorAll('tr').length / rowsPerPage
        );
        if (currentPage < totalPages) goToPage(currentPage + 1);
    });
    
    function goToPage(page) {
        currentPage = page;
        updatePagination();
    }
    
    // Helper functions
    function getColumnIndex(columnName) {
        const headers = Array.from(document.querySelectorAll('th'));
        return headers.findIndex(header => header.dataset.sort === columnName);
    }
    
    function isSameDay(d1, d2) {
        return d1.toDateString() === d2.toDateString();
    }
    
    function isWithinDays(date, reference, days) {
        const diffTime = reference - date;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays >= 0 && diffDays <= days;
    }
    
    // Initial pagination
    updatePagination();
});