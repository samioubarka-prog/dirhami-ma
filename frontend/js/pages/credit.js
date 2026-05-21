// ==================== CRÉDIT IMMOBILIER ====================
let costChart = null;
let mortgageRates = [];

document.addEventListener('DOMContentLoaded', function() {
    calculateMortgage();
    loadMortgageRates();
});

function calculateMortgage() {
    const price = parseFloat(document.getElementById('propertyPrice').value) || 0;
    const downPaymentPercent = parseFloat(document.getElementById('downPayment').value) || 0;
    const durationYears = parseFloat(document.getElementById('duration').value) || 0;
    const rate = parseFloat(document.getElementById('interestRate').value) || 0;
    const insuranceRate = parseFloat(document.getElementById('insuranceRate').value) || 0;
    const income = parseFloat(document.getElementById('income').value) || 0;

    const loanAmount = price * (1 - downPaymentPercent / 100);
    const downPaymentAmount = price - loanAmount;
    const durationMonths = durationYears * 12;
    const monthlyRate = rate / 100 / 12;

    let monthlyPayment;
    if (monthlyRate > 0) {
        monthlyPayment = loanAmount * (monthlyRate * Math.pow(1 + monthlyRate, durationMonths)) / 
                        (Math.pow(1 + monthlyRate, durationMonths) - 1);
    } else {
        monthlyPayment = loanAmount / durationMonths;
    }

    const insuranceMonthly = loanAmount * (insuranceRate / 100) / 12;
    const totalMonthly = monthlyPayment + insuranceMonthly;
    const debtRatio = (totalMonthly / income) * 100;
    const totalCost = totalMonthly * durationMonths;
    const totalInterest = (monthlyPayment * durationMonths) - loanAmount;
    const taeg = rate + (insuranceRate * 0.5);

    // Afficher les résultats
    document.getElementById('monthlyPayment').textContent = formatCurrency(monthlyPayment);
    document.getElementById('insuranceMonthly').textContent = formatCurrency(insuranceMonthly);
    document.getElementById('totalMonthly').textContent = formatCurrency(totalMonthly);
    document.getElementById('debtRatio').textContent = debtRatio.toFixed(1) + '%';
    document.getElementById('loanAmount').textContent = formatCurrency(loanAmount);
    document.getElementById('totalCost').textContent = formatCurrency(totalCost);
    document.getElementById('totalInterest').textContent = formatCurrency(totalInterest);
    document.getElementById('taeg').textContent = taeg.toFixed(2) + '%';

    // Éligibilité
    const alertEl = document.getElementById('eligibilityAlert');
    if (debtRatio > 50) {
        alertEl.className = 'alert alert-danger';
        alertEl.innerHTML = `<i class="fas fa-exclamation-circle"></i> <span>Taux d'endettement de ${debtRatio.toFixed(1)}% dépasse le plafond de 50%. Augmentez votre apport ou réduisez le montant emprunté.</span>`;
    } else if (debtRatio > 45 && income <= 20000) {
        alertEl.className = 'alert alert-warning';
        alertEl.innerHTML = `<i class="fas fa-exclamation-triangle"></i> <span>Taux d'endettement de ${debtRatio.toFixed(1)}% dépasse le plafond de 45% pour les revenus ≤ 20 000 DH.</span>`;
    } else {
        alertEl.className = 'alert alert-success';
        alertEl.innerHTML = `<i class="fas fa-check-circle"></i> <span>Votre dossier est éligible ! Taux d'endettement dans les normes.</span>`;
    }

    // Graphique de répartition
    updateCostChart(loanAmount, totalInterest, insuranceMonthly * durationMonths);

    // Tableau d'amortissement
    generateAmortizationTable(loanAmount, monthlyRate, monthlyPayment, insuranceMonthly, durationMonths);
}

function updateCostChart(principal, interest, insurance) {
    const ctx = document.getElementById('costChart');
    if (!ctx) return;

    if (costChart) costChart.destroy();

    costChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Capital remboursé', 'Intérêts', 'Assurance'],
            datasets: [{
                data: [principal, interest, insurance],
                backgroundColor: ['#1a5f2a', '#e63946', '#c9a227'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const val = context.raw;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = ((val / total) * 100).toFixed(1);
                            return formatCurrency(val) + ' (' + pct + '%)';
                        }
                    }
                }
            }
        }
    });
}

function generateAmortizationTable(loanAmount, monthlyRate, monthlyPayment, insuranceMonthly, durationMonths) {
    const tbody = document.getElementById('amortizationBody');
    if (!tbody) return;

    let remaining = loanAmount;
    let rows = '';

    for (let year = 1; year <= durationMonths / 12; year++) {
        let yearPrincipal = 0;
        let yearInterest = 0;
        let yearInsurance = 0;

        for (let month = 1; month <= 12; month++) {
            const monthIndex = (year - 1) * 12 + month;
            if (monthIndex > durationMonths) break;

            const interest = remaining * monthlyRate;
            const principal = monthlyPayment - interest;
            remaining -= principal;

            yearPrincipal += principal;
            yearInterest += interest;
            yearInsurance += insuranceMonthly;
        }

        rows += `
            <tr>
                <td><strong>${year}</strong></td>
                <td>${formatCurrency(monthlyPayment + insuranceMonthly)}</td>
                <td>${formatCurrency(yearPrincipal)}</td>
                <td>${formatCurrency(yearInterest)}</td>
                <td>${formatCurrency(yearInsurance)}</td>
                <td>${formatCurrency(Math.max(remaining, 0))}</td>
            </tr>
        `;
    }

    tbody.innerHTML = rows;
}

async function loadMortgageRates() {
    try {
        const response = await fetch('../../backend/app/data/mortgage_rates.json');
        mortgageRates = await response.json();

        const select = document.getElementById('compareBanks');
        const banks = [...new Set(mortgageRates.map(r => r.bank_name))];
        banks.forEach(bank => {
            const option = document.createElement('option');
            option.value = bank;
            option.textContent = bank;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Erreur chargement taux:', error);
    }
}

function compareBanks() {
    const select = document.getElementById('compareBanks');
    const selectedBanks = Array.from(select.selectedOptions).map(o => o.value);

    if (selectedBanks.length === 0) {
        alert('Sélectionnez au moins une banque');
        return;
    }

    const selected = mortgageRates.filter(r => selectedBanks.includes(r.bank_name));

    const container = document.getElementById('banksComparison');
    container.innerHTML = `
        <div class="comparison-table-wrapper">
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Banque</th>
                        <th>Produit</th>
                        <th>TAEG min</th>
                        <th>TAEG max</th>
                        <th>Assurance</th>
                        <th>Frais dossier</th>
                        <th>Salaire min</th>
                        <th>Âge max fin</th>
                    </tr>
                </thead>
                <tbody>
                    ${selected.map(r => `
                        <tr>
                            <td><strong>${r.bank_name}</strong></td>
                            <td>${r.product_name}</td>
                            <td>${r.taeg_min}%</td>
                            <td>${r.taeg_max}%</td>
                            <td>${r.life_insurance_rate}%</td>
                            <td>${r.application_fee_mad} DH</td>
                            <td>${r.min_salary_mad} DH</td>
                            <td>${r.max_age_at_end} ans</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}
