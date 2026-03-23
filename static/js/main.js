let currentFilter = 'Todas';
let currentPage = 1;
const limit = 50;
let myChart = null;

document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadTransactions();
    setupEventListeners();
});

function setupEventListeners() {
    // Filter Buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            currentFilter = e.target.dataset.filter;
            currentPage = 1; // Reset to page 1 on new filter
            loadTransactions();
        });
    });

    // Pagination
    document.getElementById('prev-page').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadTransactions();
        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        currentPage++;
        loadTransactions();
    });
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

function formatNumber(value) {
    return new Intl.NumberFormat('pt-BR').format(value);
}

async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        if (response.ok) {
            document.getElementById('total-transacoes').textContent = formatNumber(data.total_transacoes);
            document.getElementById('total-legitimas').textContent = formatNumber(data.total_legitimas);
            document.getElementById('total-fraudes').textContent = formatNumber(data.total_fraudes);
            document.getElementById('valor-fraudes').textContent = formatCurrency(data.valor_fraudes);
            
            updateChart(data.total_legitimas, data.total_fraudes);
        } else {
            console.error('API Error:', data.error);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

async function loadTransactions() {
    try {
        const offset = (currentPage - 1) * limit;
        const response = await fetch(`/api/transactions?filter=${currentFilter}&limit=${limit}&offset=${offset}`);
        const data = await response.json();

        if (response.ok) {
            renderTable(data);
            
            // Update pagination UI
            document.getElementById('page-info').textContent = `Página ${currentPage}`;
            document.getElementById('prev-page').disabled = currentPage === 1;
            
            // Disable next if we received fewer items than requested (end of data)
            document.getElementById('next-page').disabled = data.length < limit;
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

function renderTable(transactions) {
    const tbody = document.getElementById('transactions-body');
    tbody.innerHTML = '';

    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-secondary);">Nenhuma transação encontrada.</td></tr>';
        return;
    }

    transactions.forEach(t => {
        const isFraud = t.Class === 1;
        const statusBadge = isFraud 
            ? '<span class="status-badge status-fraud">Fraude detectada</span>'
            : '<span class="status-badge status-legit">Legítima</span>';
            
        const time = t.Time !== undefined ? t.Time : '-';
        const amount = t.Amount !== undefined ? formatCurrency(t.Amount) : '-';

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${isFraud ? '🚨' : '✅'} ${t.is_fraud}</td>
            <td style="color: var(--text-secondary);">${time}</td>
            <td style="font-family: monospace; font-size: 1rem;">${amount}</td>
            <td>${statusBadge}</td>
        `;
        tbody.appendChild(row);
    });
}

function updateChart(legit, fraud) {
    const ctx = document.getElementById('distributionChart').getContext('2d');
    
    if (myChart) {
        myChart.destroy();
    }

    Chart.defaults.color = '#8b949e';
    Chart.defaults.font.family = "'Inter', sans-serif";

    myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Legítimas', 'Fraudes'],
            datasets: [{
                data: [legit, fraud],
                backgroundColor: [
                    'rgba(63, 185, 80, 0.8)',
                    'rgba(248, 81, 73, 0.8)'
                ],
                borderColor: [
                    '#3fb950',
                    '#f85149'
                ],
                borderWidth: 1,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(22, 27, 34, 0.9)',
                    titleColor: '#e6edf3',
                    bodyColor: '#e6edf3',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    padding: 12,
                    boxPadding: 6
                }
            },
            cutout: '70%'
        }
    });
}
