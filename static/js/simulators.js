// ========== UTILITAIRES ==========
function formatMAD(amount) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'MAD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function updateRange(inputId, displayId) {
    const input = document.getElementById(inputId);
    const display = document.getElementById(displayId);
    let val = input.value;
    if (inputId.includes('rate') || inputId.includes('return')) {
        display.textContent = val + '%';
    } else if (inputId.includes('years')) {
        display.textContent = val + ' ans';
    } else {
        display.textContent = val;
    }
}

function switchTab(tabName) {
    document.querySelectorAll('.sim-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.sim-panel').forEach(p => p.classList.remove('active'));
    document.getElementById('tab-' + tabName).classList.add('active');
    document.getElementById('panel-' + tabName).classList.add('active');

    // Update URL
    const url = new URL(window.location);
    url.searchParams.set('type', tabName);
    window.history.replaceState({}, '', url);
}

// Check URL params on load
document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const type = params.get('type');
    if (type && ['investment', 'loan', 'retirement'].includes(type)) {
        switchTab(type);
    }
});

// ========== CHARTS STORAGE ==========
let invChart = null;
let loanChart = null;
let retChart = null;

// ========== INVESTMENT SIMULATOR ==========
async function calculateInvestment() {
    const btn = document.getElementById('inv-btn-text');
    btn.textContent = 'Calcul en cours...';

    const data = {
        initial_amount: parseFloat(document.getElementById('inv-initial').value) || 0,
        monthly_contribution: parseFloat(document.getElementById('inv-monthly').value) || 0,
        annual_rate: parseFloat(document.getElementById('inv-rate').value) || 0,
        years: parseInt(document.getElementById('inv-years').value) || 1,
        compound_frequency: 12
    };

    try {
        const res = await fetch('/api/calculators/investment', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const result = await res.json();

        // Display results
        document.getElementById('inv-final').textContent = formatMAD(result.final_amount);
        document.getElementById('inv-gain').textContent = formatMAD(result.total_return);
        document.getElementById('inv-total').textContent = formatMAD(result.total_contributed);

        // Chart
        const labels = result.yearly_projection.map(p => 'Annee ' + p.year);
        const contributions = result.yearly_projection.map(p => p.contributions);
        const balances = result.yearly_projection.map(p => p.balance);

        if (invChart) invChart.destroy();

        const ctx = document.getElementById('inv-chart').getContext('2d');
        invChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Capital total',
                        data: balances,
                        borderColor: '#1a5f2a',
                        backgroundColor: 'rgba(26, 95, 42, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Versements',
                        data: contributions,
                        borderColor: '#64748b',
                        backgroundColor: 'rgba(100, 116, 139, 0.1)',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + formatMAD(context.raw);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: {
                            callback: function(value) {
                                return formatMAD(value);
                            }
                        }
                    }
                }
            }
        });

        // Table
        const tableHtml = `
            <table>
                <thead>
                    <tr>
                        <th>Annee</th>
                        <th>Capital</th>
                        <th>Versements</th>
                        <th>Gains</th>
                        <th>Gain de l'annee</th>
                    </tr>
                </thead>
                <tbody>
                    ${result.yearly_projection.map(p => `
                        <tr>
                            <td>${p.year}</td>
                            <td><strong>${formatMAD(p.balance)}</strong></td>
                            <td>${formatMAD(p.contributions)}</td>
                            <td>${formatMAD(p.returns)}</td>
                            <td>${formatMAD(p.return_year)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        document.getElementById('inv-table').innerHTML = tableHtml;

    } catch (e) {
        console.error('Erreur calcul investissement:', e);
        alert('Erreur lors du calcul. Veuillez reessayer.');
    } finally {
        btn.textContent = 'Calculer';
    }
}

// ========== LOAN SIMULATOR ==========
async function calculateLoan() {
    const btn = document.getElementById('loan-btn-text');
    btn.textContent = 'Calcul en cours...';

    const data = {
        amount: parseFloat(document.getElementById('loan-amount').value) || 0,
        rate: parseFloat(document.getElementById('loan-rate').value) || 0,
        years: parseInt(document.getElementById('loan-years').value) || 1,
        type: document.getElementById('loan-type').value
    };

    try {
        const res = await fetch('/api/calculators/loan', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const result = await res.json();

        // Display results
        document.getElementById('loan-monthly').textContent = formatMAD(result.monthly_payment);
        document.getElementById('loan-cost').textContent = formatMAD(result.total_cost);
        document.getElementById('loan-interest').textContent = formatMAD(result.total_interest);

        // Chart
        if (loanChart) loanChart.destroy();

        if (result.type === 'amortissable') {
            const ctx = document.getElementById('loan-chart').getContext('2d');

            // Group by year
            const yearlyData = {};
            result.schedule.forEach(row => {
                const year = row.year;
                if (!yearlyData[year]) {
                    yearlyData[year] = { principal: 0, interest: 0 };
                }
                yearlyData[year].principal += row.principal;
                yearlyData[year].interest += row.interest;
            });

            const years = Object.keys(yearlyData);
            const principals = years.map(y => yearlyData[y].principal);
            const interests = years.map(y => yearlyData[y].interest);

            loanChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: years.map(y => 'Annee ' + y),
                    datasets: [
                        {
                            label: 'Capital rembourse',
                            data: principals,
                            backgroundColor: '#1a5f2a'
                        },
                        {
                            label: 'Interets',
                            data: interests,
                            backgroundColor: '#dc2626'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'top' },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.dataset.label + ': ' + formatMAD(context.raw);
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            ticks: { callback: function(value) { return formatMAD(value); } }
                        },
                        x: { stacked: true },
                        y: { stacked: true }
                    }
                }
            });

            // Amortization table
            const tableHtml = `
                <h3>Tableau d'amortissement</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Mois</th>
                            <th>Mensualite</th>
                            <th>Capital</th>
                            <th>Interets</th>
                            <th>Restant du</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.schedule.map(row => `
                            <tr>
                                <td>${row.month}</td>
                                <td>${formatMAD(row.payment)}</td>
                                <td>${formatMAD(row.principal)}</td>
                                <td>${formatMAD(row.interest)}</td>
                                <td>${formatMAD(row.balance)}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            document.getElementById('loan-table').innerHTML = tableHtml;
        } else {
            // In fine - simple display
            document.getElementById('loan-chart').style.display = 'none';
            document.getElementById('loan-table').innerHTML = `
                <div class="info-box">
                    <h3>Pret In Fine</h3>
                    <p>Vous payez <strong>${formatMAD(result.monthly_payment)}</strong> d'interets chaque mois.</p>
                    <p>A la fin des ${result.years} ans, vous remboursez le capital de <strong>${formatMAD(result.final_payment)}</strong>.</p>
                </div>
            `;
        }

    } catch (e) {
        console.error('Erreur calcul pret:', e);
        alert('Erreur lors du calcul. Veuillez reessayer.');
    } finally {
        btn.textContent = 'Calculer';
    }
}

// ========== RETIREMENT SIMULATOR ==========
async function calculateRetirement() {
    const btn = document.getElementById('ret-btn-text');
    btn.textContent = 'Calcul en cours...';

    const data = {
        current_age: parseInt(document.getElementById('ret-current').value) || 30,
        retirement_age: parseInt(document.getElementById('ret-age').value) || 60,
        monthly_savings: parseFloat(document.getElementById('ret-monthly').value) || 0,
        current_savings: parseFloat(document.getElementById('ret-savings').value) || 0,
        expected_return: parseFloat(document.getElementById('ret-return').value) || 6
    };

    try {
        const res = await fetch('/api/calculators/retirement', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const result = await res.json();

        // Display results
        document.getElementById('ret-capital').textContent = formatMAD(result.capital_at_retirement);
        document.getElementById('ret-pension').textContent = formatMAD(result.estimated_monthly_pension);
        document.getElementById('ret-years').textContent = result.years_to_retire + ' ans';

        // Chart
        if (retChart) retChart.destroy();

        const ctx = document.getElementById('ret-chart').getContext('2d');
        const labels = result.projection.map(p => p.age + ' ans');
        const balances = result.projection.map(p => p.balance);
        const savings = result.projection.map(p => p.total_saved);

        retChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Capital projete',
                        data: balances,
                        borderColor: '#1a5f2a',
                        backgroundColor: 'rgba(26, 95, 42, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Versements cumules',
                        data: savings,
                        borderColor: '#c9a227',
                        backgroundColor: 'rgba(201, 162, 39, 0.1)',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + formatMAD(context.raw);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: { callback: function(value) { return formatMAD(value); } }
                    }
                }
            }
        });

        // Table
        const tableHtml = `
            <h3>Projection par age</h3>
            <table>
                <thead>
                    <tr>
                        <th>Age</th>
                        <th>Capital</th>
                        <th>Versements</th>
                        <th>Gains</th>
                        <th>Reste</th>
                    </tr>
                </thead>
                <tbody>
                    ${result.projection.map(p => `
                        <tr>
                            <td><strong>${p.age} ans</strong></td>
                            <td>${formatMAD(p.balance)}</td>
                            <td>${formatMAD(p.total_saved)}</td>
                            <td>${formatMAD(p.returns)}</td>
                            <td>${p.years_remaining} ans</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        document.getElementById('ret-table').innerHTML = tableHtml;

    } catch (e) {
        console.error('Erreur calcul retraite:', e);
        alert('Erreur lors du calcul. Veuillez reessayer.');
    } finally {
        btn.textContent = 'Calculer';
    }
}
