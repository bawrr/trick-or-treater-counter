// Ensure the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Cumulative Graph
    const ctxCumulative = document.getElementById('cumulativeChart').getContext('2d');
    const cumulativeChart = new Chart(ctxCumulative, {
        type: 'line',
        data: {
            labels: cumulativeData.labels,
            datasets: [{
                label: 'Cumulative Trick-or-Treaters',
                data: cumulativeData.counts,
                backgroundColor: 'rgba(255, 117, 24, 0.2)',
                borderColor: 'rgba(255, 117, 24, 1)',
                borderWidth: 2,
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time' } },
                y: { title: { display: true, text: 'Total Trick-or-Treaters' }, beginAtZero: true }
            }
        }
    });

    // Count Graph
    const ctxCount = document.getElementById('countChart').getContext('2d');
    const countChart = new Chart(ctxCount, {
        type: 'bar',
        data: {
            labels: countData.labels,
            datasets: [{
                label: 'Trick-or-Treaters per 15 Minutes',
                data: countData.counts,
                backgroundColor: 'rgba(23, 162, 184, 0.5)',
                borderColor: 'rgba(23, 162, 184, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time' } },
                y: { title: { display: true, text: 'Number of Trick-or-Treaters' }, beginAtZero: true }
            }
        }
    });
});
