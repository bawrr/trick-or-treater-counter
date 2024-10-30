function confirmReset() {
    if (confirm('Are you sure you want to reset the data?')) {
        document.getElementById('confirm-reset').value = 'yes';
        document.getElementById('reset-form').submit();
    }
}
