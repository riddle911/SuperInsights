function filterByDate(date) {
    window.location.href = `/?date=${date}`;
}

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const dateFilter = urlParams.get('date');
    if (dateFilter) {
        document.getElementById('dateFilter').value = dateFilter;
    }
});
