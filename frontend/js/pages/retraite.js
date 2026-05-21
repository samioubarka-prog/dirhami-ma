// ==================== RETRAITE ====================
let retirementChart = null;

document.addEventListener('DOMContentLoaded', calculateRetirement);

function calculateRetirement() {
    const currentAge = parseInt(document.getElementById('currentAge').value) || 35;
    const retirementAge = parseInt(document.getElementById('retirementAge').value) || 60;
    const currentSalary = parseFloat(document.getElementById('currentSalary').value) || 0;
    const currentSavings = parseFloat(document.getElementById('currentSavings').value) || 0;
    const monthlyContribution = parseFloat(document.getElementById('monthlyContribution').value) || 0;
    const expectedReturn = parseFloat(document.getElementById('expectedReturn').value) || 0;
    const inflation = parseFloat(document.getElementById('inflation').value) || 0;
    const replacementRate = parseFloat(document.getElementById('replacementRate').value) || 70;
    const lifeExpectancy = parseInt(document.getElementById('lifeExpectancy').value) || 85;

    const yearsToRetirement = retirementAge - currentAge;
    const remainingYears = lifeExpectancy - retirementAge;
    const realReturn = (expectedReturn / 100) - (inflation / 100);
    const monthlyRealReturn = realReturn / 12;

    // Capital accumulé
    let accumulated = currentSavings;
    const yearlyData = [];

    for (let year = 1; year <= yearsToRetirement; year++) {
        for (let month = 1; month <= 12; month++) {
            accumulated = accumulated * (1 + monthlyRealReturn) + monthlyContribution;
        }

        const adjustedSalary = currentSalary * Math.pow(1 + inflation / 100, year);

        yearlyData.push({
            year: currentAge + year,
            accumulated: accumulated,
            salary: adjustedSalary
        });
    }

    // Pension mensuelle
    let monthlyPension;
    if (remainingYears > 0 && realReturn > 0) {
        monthlyPension = accumulated * (monthlyRealReturn * Math.pow(1 + monthlyRealReturn, remainingYears * 12)) /
                        (Math.pow(1 + monthlyRealReturn, remainingYears * 12) - 1);
    } else {
        monthlyPension = accumulated / (remainingYears * 12);
    }

    const desiredPension = currentSalary * (replacementRate / 100);
    const pensionGap = Math.max(desiredPension - monthlyPension, 0);
    const actualReplacement = (monthlyPension / currentSalary) * 100;
    const isOnTrack = monthlyPension >= desiredPension;

    // Contribution recommandée
    let recommendedContribution = monthlyContribution;
    if (pensionGap > 0 && yearsToRetirement > 0 && realReturn > 0) {
        const n = yearsToRetirement * 12;
        recommendedContribution = (pensionGap * (Math.pow(1 + monthlyRealReturn, n) - 1)) /
                                 (monthlyRealReturn * Math.pow(1 + monthlyRealReturn, n));
        recommendedContribution = recommendedContribution / 12;
    }

    // Afficher résultats
    document.getElementById('yearsToRetirement').textContent = yearsToRetirement;
    document.getElementById('totalAccumulated').textContent = formatCurrency(accumulated);
    document.getElementById('monthlyPension').textContent = formatCurrency(monthlyPension);
    document.getElementById('desiredPension').textContent = formatCurrency(desiredPension);
    document.getElementById('pensionGap').textContent = formatCurrency(pensionGap);
    document.getElementById('actualReplacement').textContent = actualReplacement.toFixed(0) + '%';

    const alertEl = document.getElementById('retirementAlert');
    if (isOnTrack) {
        alertEl.className = 'alert alert-success';
        alertEl.innerHTML = '<i class="fas fa-check-circle"></i> <span>Bravo ! Vous êtes sur la bonne voie pour une retraite sereine.</span>';
        document.getElementById('recommendedContributionCard').style.display = 'none';
    } else {
        alertEl.className = 'alert alert-warning';
        alertEl.innerHTML = `<i class="fas fa-exclamation-triangle"></i> <span>Vous avez un écart de ${formatCurrency(pensionGap)}. Augmentez vos versements pour atteindre votre objectif.</span>`;
        document.getElementById('recommendedContributionCard').style.display = 'block';
        document.getElementById('recommendedContribution').textContent = formatCurrency(recommendedContribution) + '/mois';
    }

    // Graphique
    updateRetirementChart(yearlyData);
}

function updateRetirementChart(data) {
    const ctx = document.getElementById('retirementChart');
    if (!ctx) return;

    if (retirementChart) retirementChart.destroy();

    retirementChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.year + ' ans'),
            datasets: [{
                label: 'Capital accumulé',
                data: data.map(d => d.accumulated),
                borderColor: '#1a5f2a',
                backgroundColor: 'rgba(26, 95, 42, 0.1)',
                fill: true,
                tension: 0.4
            }, {
                label: 'Salaire projeté',
                data: data.map(d => d.salary * 12),
                borderColor: '#c9a227',
                backgroundColor: 'transparent',
                borderDash: [5, 5],
                tension: 0.4
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
                            return context.dataset.label + ': ' + formatCurrency(context.raw);
                        }
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        callback: function(value) {
                            return (value / 1000000).toFixed(1) + 'M DH';
                        }
                    }
                }
            }
        }
    });
}
