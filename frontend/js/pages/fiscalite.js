// ==================== FISCALITÉ ====================
let taxRegimes = [];

document.addEventListener('DOMContentLoaded', loadTaxRegimes);

async function loadTaxRegimes() {
    showLoading('taxGrid');

    try {
        const response = await fetch('../../backend/app/data/tax_regimes.json');
        taxRegimes = await response.json();
        renderTaxRegimes(taxRegimes);
    } catch (error) {
        showError('taxGrid', 'Erreur lors du chargement des régimes fiscaux');
    }
}

function renderTaxRegimes(regimes) {
    const grid = document.getElementById('taxGrid');

    grid.innerHTML = regimes.map(regime => `
        <div class="tax-card">
            <div class="tax-card-header">
                <h3>${regime.name}</h3>
                <span class="tax-type">${regime.regime_type}</span>
            </div>
            <div class="tax-card-body">
                <div class="tax-benefit">
                    <i class="fas fa-percentage"></i>
                    <span class="benefit-label">Déduction fiscale</span>
                    <span class="benefit-value">${regime.tax_deduction_percent > 0 ? regime.tax_deduction_percent + '%' : 'N/A'}</span>
                </div>
                <div class="tax-benefit">
                    <i class="fas fa-money-bill-wave"></i>
                    <span class="benefit-label">Plafond déduction</span>
                    <span class="benefit-value">${regime.tax_deduction_max_mad > 0 ? formatCurrency(regime.tax_deduction_max_mad) + '/an' : 'N/A'}</span>
                </div>
                <div class="tax-benefit">
                    <i class="fas fa-clock"></i>
                    <span class="benefit-label">Durée blocage</span>
                    <span class="benefit-value">${regime.lock_up_period_years > 0 ? regime.lock_up_period_years + ' ans' : 'Aucune'}</span>
                </div>
                <div class="tax-benefit">
                    <i class="fas fa-users"></i>
                    <span class="benefit-label">Profils éligibles</span>
                    <span class="benefit-value">${regime.eligible_profiles ? regime.eligible_profiles.join(', ') : 'Tous'}</span>
                </div>
                <div class="tax-benefit">
                    <i class="fas fa-hand-holding-usd"></i>
                    <span class="benefit-label">Min. souscription</span>
                    <span class="benefit-value">${regime.min_subscription_mad > 0 ? formatCurrency(regime.min_subscription_mad) : 'Aucun'}</span>
                </div>
                <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--gray-200);">
                    <p style="font-size: 0.9rem; color: var(--gray-600); line-height: 1.6;">${regime.description}</p>
                </div>
            </div>
        </div>
    `).join('');
}

function calculateTaxDeduction() {
    const regimeCode = document.getElementById('taxRegimeSelect').value;
    const amount = parseFloat(document.getElementById('taxAmount').value) || 0;
    const annualIncome = parseFloat(document.getElementById('annualIncome').value) || 0;

    const regime = taxRegimes.find(r => r.code === regimeCode);
    if (!regime) return;

    const deductionPercent = regime.tax_deduction_percent;
    const maxDeduction = regime.tax_deduction_max_mad;

    const calculatedDeduction = amount * (deductionPercent / 100);
    const actualDeduction = maxDeduction > 0 ? Math.min(calculatedDeduction, maxDeduction) : calculatedDeduction;

    // Économie d'impôt (taux marginal 30% pour simplifier)
    const taxSavings = actualDeduction * 0.30;
    const effectiveReturn = amount > 0 ? (taxSavings / amount) * 100 : 0;

    document.getElementById('deductionRate').textContent = deductionPercent + '%';
    document.getElementById('calculatedDeduction').textContent = formatCurrency(calculatedDeduction);
    document.getElementById('maxDeduction').textContent = maxDeduction > 0 ? formatCurrency(maxDeduction) : 'Illimité';
    document.getElementById('actualDeduction').textContent = formatCurrency(actualDeduction);
    document.getElementById('taxSavings').textContent = formatCurrency(taxSavings);
    document.getElementById('effectiveReturn').textContent = effectiveReturn.toFixed(1) + '%';
}
