async function initDashboard() {
    try {
        const response = await fetch('data.json');
        const data = await response.json();
        
        // Update Metrics
        document.getElementById('stat-total').textContent = data.total.toLocaleString();
        document.getElementById('stat-submitted').textContent = data.submitted.toLocaleString();
        document.getElementById('stat-billionaire').textContent = (data.billionaireOutreach || 0).toLocaleString();
        document.getElementById('stat-agents').textContent = "10";
        
        // Populate Activity Feed (Mocking real dates from data)
        const tableBody = document.querySelector('#activity-table tbody');
        const companies = Object.keys(data.companies).slice(0, 10);
        
        companies.forEach(company => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>2026-05-02</td>
                <td style="font-weight: 600;">${company}</td>
                <td>Strategy & Ops</td>
                <td><span class="status-tag submitted">Verified</span></td>
            `;
            tableBody.appendChild(row);
        });

        // Initialize Velocity Chart
        const ctx = document.getElementById('velocityChart').getContext('2d');
        
        // Sort timeline keys
        const dates = Object.keys(data.timeline).sort();
        const counts = dates.map(d => data.timeline[d]);

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates.map(d => d.split('-').slice(1).join('/')),
                datasets: [{
                    label: 'Submissions',
                    data: counts,
                    borderColor: '#00f2ff',
                    backgroundColor: 'rgba(0, 242, 255, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#00f2ff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });

    } catch (error) {
        console.error('Failed to load dashboard data:', error);
    }
}

document.addEventListener('DOMContentLoaded', initDashboard);
