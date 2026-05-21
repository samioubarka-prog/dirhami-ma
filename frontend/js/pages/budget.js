// ==================== BUDGET ====================
let budgetChart = null;

document.addEventListener('DOMContentLoaded', function() {
    // Auto-calculate on load
    analyzeBudget();
});

function analyzeBudget() {
    const income = parseFloat(document.getElementById('incomeSalary').value) || 0;
    const extraIncome = parseFloat(document.getElementById('incomeExtra').value) || 0;
    const housing = parseFloat(document.getElementById('expenseHousing').value) || 0;
    const transport = parseFloat(document.getElementById('expenseTransport').value) || 0;
    const food = parseFloat(document.getElementById('expenseFood').value) || 0;
    const health = parseFloat(document.getElementById('expenseHealth').value) || 0;
    const education = parseFloat(document.getElementById('expenseEducation').value) || 0;
    const leisure = parseFloat(document.getElementById('expenseLeisure').value) || 0;
    const savings = parseFloat(document.getElementById('expenseSavings').value) || 0;
    const other = parseFloat(document.getElementById('expenseOther').value) || 0;

    const totalIncome = income + extraIncome;
    const totalExpenses = housing + transport + food + health + education + leisure + savings + other;
    const remaining = totalIncome - totalExpenses;
    const savingsRate = totalIncome > 0 ? (savings / totalIncome) * 100 : 0;

    // Afficher résultats
    document.getElementById('totalIncome').textContent = formatCurrency(totalIncome);
    document.getElementById('totalExpenses').textContent = formatCurrency(totalExpenses);
    document.getElementById('remainingBudget').textContent = formatCurrency(remaining);
    document.getElementById('savingsRate').textContent = savingsRate.toFixed(1) + '%';

    document.getElementById('budgetResult').style.display = 'block';

    // Graphique
    updateBudgetChart(housing, transport, food, health, education, leisure, savings, other, remaining > 0 ? remaining : 0);

    // Recommandations
    generateRecommendations(totalIncome, housing, transport, food, leisure, savings, remaining);

    // Potentiel d'économies
    generateSavingsPotential(totalIncome, housing, transport, food, leisure);
}

function updateBudgetChart(housing, transport, food, health, education, leisure, savings, other, remaining) {
    const ctx = document.getElementById('budgetChart');
    if (!ctx) return;

    if (budgetChart) budgetChart.destroy();

    budgetChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Logement', 'Transport', 'Alimentation', 'Santé', 'Éducation', 'Loisirs', 'Épargne', 'Autres', 'Solde'],
            datasets: [{
                data: [housing, transport, food, health, education, leisure, savings, other, remaining],
                backgroundColor: [
                    '#e63946', '#f4a261', '#2a9d8f', '#e9c46a', 
                    '#264653', '#f4a261', '#1a5f2a', '#6c757d', '#c9a227'
                ],
                borderWidth: 2,
                borderColor: '#fff'
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
                            return context.label + ': ' + formatCurrency(val) + ' (' + pct + '%)';
                        }
                    }
                }
            }
        }
    });
}

function generateRecommendations(totalIncome, housing, transport, food, leisure, savings, remaining) {
    const recommendations = [];

    const needs = housing + transport + food;
    const wants = leisure;
    const needsPercent = (needs / totalIncome) * 100;
    const wantsPercent = (wants / totalIncome) * 100;

    if (needsPercent > 50) {
        recommendations.push({
            type: 'warning',
            text: `Vos besoins essentiels représentent ${needsPercent.toFixed(0)}% de vos revenus (recommandé: 50%). Envisagez de réduire vos dépenses de logement ou transport.`
        });
    }

    if (wantsPercent > 30) {
        recommendations.push({
            type: 'warning',
            text: `Vos dépenses discrétionnaires représentent ${wantsPercent.toFixed(0)}% de vos revenus (recommandé: 30%). Opportunité d'économiser ${formatCurrency(wants - totalIncome * 0.3)}.`
        });
    }

    const savingsRate = (savings / totalIncome) * 100;
    if (savingsRate < 20) {
        recommendations.push({
            type: 'warning',
            text: `Votre taux d'épargne est de ${savingsRate.toFixed(0)}% (recommandé: 20%). Augmentez votre épargne de ${formatCurrency(totalIncome * 0.2 - savings)} pour atteindre 20%.`
        });
    } else {
        recommendations.push({
            type: 'success',
            text: `Excellent ! Vous épargnez ${savingsRate.toFixed(0)}% de vos revenus. Continuez sur cette lancée !`
        });
    }

    if (remaining < 0) {
        recommendations.push({
            type: 'danger',
            text: `⚠️ Vous êtes en déficit de ${formatCurrency(Math.abs(remaining))} ! Réduisez immédiatement vos dépenses ou augmentez vos revenus.`
        });
    }

    const list = document.getElementById('recommendationsList');
    list.innerHTML = recommendations.map(r => `
        <div class="recommendation-card ${r.type}">
            <i class="fas fa-${r.type === 'success' ? 'check-circle' : r.type === 'danger' ? 'exclamation-circle' : 'exclamation-triangle'}"></i>
            <span>${r.text}</span>
        </div>
    `).join('');
}

function generateSavingsPotential(totalIncome, housing, transport, food, leisure) {
    const potentials = [];

    // Alimentation
    if (food > totalIncome * 0.15) {
        potentials.push({
            category: 'Alimentation',
            current: food,
            recommended: totalIncome * 0.15,
            potential: food - totalIncome * 0.15,
            tips: ['Faire les courses avec une liste', 'Cuisiner à la maison', 'Éviter le gaspillage']
        });
    }

    // Transport
    if (transport > totalIncome * 0.10) {
        potentials.push({
            category: 'Transport',
            current: transport,
            recommended: totalIncome * 0.10,
            potential: transport - totalIncome * 0.10,
            tips: ['Utiliser les transports en commun', 'Covoiturage', 'Vélo pour courts trajets']
        });
    }

    // Loisirs
    if (leisure > totalIncome * 0.10) {
        potentials.push({
            category: 'Loisirs',
            current: leisure,
            recommended: totalIncome * 0.10,
            potential: leisure - totalIncome * 0.10,
            tips: ['Profiter des activités gratuites', 'Cartes de réduction', 'Planifier les sorties']
        });
    }

    // Logement
    if (housing > totalIncome * 0.30) {
        potentials.push({
            category: 'Logement',
            current: housing,
            recommended: totalIncome * 0.30,
            potential: housing - totalIncome * 0.30,
            tips: ['Négocier le loyer', 'Chercher un colocataire', 'Déménager dans zone moins chère']
        });
    }

    const list = document.getElementById('savingsPotentialList');
    if (potentials.length === 0) {
        list.innerHTML = '<div class="alert alert-success"><i class="fas fa-check-circle"></i> Vos dépenses sont bien équilibrées !</div>';
        return;
    }

    list.innerHTML = potentials.map(p => `
        <div class="savings-potential">
            <h4><i class="fas fa-piggy-bank"></i> ${p.category}</h4>
            <p>Actuel: <strong>${formatCurrency(p.current)}</strong> | Recommandé: <strong>${formatCurrency(p.recommended)}</strong></p>
            <p style="color: var(--success); font-weight: 700;">Économie potentielle: ${formatCurrency(p.potential)}</p>
            <ul>
                ${p.tips.map(t => `<li><i class="fas fa-lightbulb" style="color: var(--secondary);"></i> ${t}</li>`).join('')}
            </ul>
        </div>
    `).join('');
}
