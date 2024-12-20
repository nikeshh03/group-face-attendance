document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const dateFilter = document.getElementById('dateFilter');
    const tableBody = document.querySelector('.attendance-table tbody');
    
    // Search functionality
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        filterTable();
    });
    
    // Date filter functionality
    dateFilter.addEventListener('change', function(e) {
        filterTable();
    });
    
    function filterTable() {
        const searchTerm = searchInput.value.toLowerCase();
        const filterValue = dateFilter.value;
        
        // Make AJAX request
        const url = new URL(window.location.href);
        url.searchParams.set('search', searchTerm);
        url.searchParams.set('date_filter', filterValue);
        
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newTableBody = doc.querySelector('.attendance-table tbody');
                tableBody.innerHTML = newTableBody.innerHTML;
                
                // Update total records count
                const totalRecords = doc.querySelector('.total-records span');
                document.querySelector('.total-records span').textContent = totalRecords.textContent;
            });
    }
});