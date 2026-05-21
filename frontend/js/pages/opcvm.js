// ==================== OPCVM ====================
let allOPCVM = [];
let opcvmChart = null;

document.addEventListener('DOMContentLoaded', loadOPCVM);

async function loadOPCVM() {
    showLoading('opcvmGrid');

    try {
        const response = await fetch('../../backend/app/data/opcvm.json');
        allOPCVM = await response.json();

        // Remplir les sociétés de gestion
        const companies = [...new Set(allOPCVM.map(f => f.management_company))];
        const companySelect = document.getElementById('filterCompany');
        companies.forEach(company => {
            const option = document.createElement('option');
            option.value = company;
            option.textContent = company;
            companySelect.appendChild(option);
        });

        renderOPCVM(allOPCVM);
        simulateOPCVM();
    } catch (error) {
        showError('opcvmGrid', 'Erreur lors du chargement des OPCVM');
    }
}

function renderOPCVM(funds) {
    const grid = document.getElementById('opcvmGrid');

    if (funds.length === 0) {
        grid.innerHTML = '<div class="alert alert-info"><i class="fas fa-info-circle"></i> Aucun OPCVM ne correspond à vos critères.</div>';
        return;
    }

    grid.innerHTML = funds.map(fund => `
        <div class="opcvm-card">
            <div class="opcvm-header">
                <h3>${fund.name}</h3>
                <span class="company">${fund.management_company}</span>
            </div>
            <div class="opcvm-body">
                <div style="display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap;">
                    <span class="tag ${fund.risk_profile === 'Faible' ? 'tag-success' : fund.risk_profile === 'Modéré' ? 'tag-warning' : 'tag-info'}">${fund.risk_profile}</span>
                    <span class="tag tag-info">${fund.category}</span>
                    <span class="tag tag-warning">Min: ${fund.min_subscription_mad} DH</span>
                </div>
                <div class="return-grid">
                    <div class="return-item">
                        <div class="return-label">YTD</div>
                        <div class="return-value ${(fund.ytd_return || 0) >= 0 ? 'positive' : 'negative'}">${fund.ytd_return !== null ? fund.ytd_return + '%' : 'N/A'}</div>
                    </div>
                    <div class="return-item">
                        <div class="return-label">1 an</div>
                        <div class="return-value ${(fund.one_year_return || 0) >= 0 ? 'positive' : 'negative'}">${fund.one_year_return !== null ? fund.one_year_return + '%' : 'N/A'}</div>
                    </div>
                    <div class="return-item">
                        <div class="return-label">3 ans</div>
                        <div class="return-value ${(fund.three_year_return || 0) >= 0 ? 'positive' : 'negative'}">${fund.three_year_return !== null ? fund.three_year_return + '%' : 'N/A'}</div>
                    </div>
                    <div class="return-item">
                        <div class="return-label">5 ans</div>
                        <div class="return-value ${(fund.five_year_return || 0) >= 0 ? 'positive' : 'negative'}">${fund.five_year_return !== null ? fund.five_year_return + '%' : 'N/A'}</div>
                    </div>
                </div>
                <div class="fees-summary">
                    <div>
                        <span>Entrée: <strong>${fund.entry_fee_percent}%</strong></span>
                        <span>Gestion: <strong>${fund.management_fee_percent}%</strong></span>
                        <span>Sortie: <strong>${fund.exit_fee_percent}%</strong></span>
                    </div>
                </div>
                <div style="margin-top: 12px; font-size: 0.85rem; color: var(--gray-600);">
                    <i class="fas fa-chart-pie"></i> Allocation: ${fund.equity_percent || 0}% actions, ${fund.bond_percent || 0}% obligations, ${fund.cash_percent || 0}% liquidités
                </div>
            </div>
        </div>
    `).join('');
}

function applyOPCVMFilters() {
    const company = document.getElementById('filterCompany').value;
    const category = document.getElementById('filterCategory').value;
    const risk = document.getElementById('filterRisk').value;
    const maxEntry = document.getElementById('filterMaxEntry').value;
    const minReturn = document.getElementById('filterMinReturn').value;

    let filtered = allOPCVM;

    if (company) filtered = filtered.filter(f => f.management_company === company);
    if (category) filtered = filtered.filter(f => f.category === category);
    if (risk) filtered = filtered.filter(f => f.risk_profile === risk);
    if (maxEntry) filtered = filtered.filter(f => f.entry_fee_percent <= parseFloat(maxEntry));
    if (minReturn) filtered = filtered.filter(f => (f.one_year_return || 0) >= parseFloat(minReturn));

    renderOPCVM(filtered);
}

function resetOPCVMFilters() {
    document.getElementById('filterCompany').value = '';
    document.getElementById('filterCategory').value = '';
    document.getElementById('filterRisk').value = '';
    document.getElementById('filterMaxEntry').value = '';
    document.getElementById('filterMinReturn').value = '';
    renderOPCVM(allOPCVM);
}

function simulateOPCVM() {
    const initial = parseFloat(document.getElementById('opcvmInitial').value) || 0;
    const monthly = parseFloat(document.getElementById('opcvmMonthly').value) || 0;
    const years = parseFloat(document.getElementById('opcvmDuration').value) || 0;
    const annualReturn = parseFloat(document.getElementById('opcvmReturn').value) || 0;
    const entryFee = parseFloat(document.getElementById('opcvmEntryFee').value) || 0;
    const mgmtFee = parseFloat(document.getElementById('opcvmMgmtFee').value) || 0;

    const monthlyReturn = annualReturn / 100 / 12;
    const monthlyMgmtFee = mgmtFee / 100 / 12;

    // Frais d'entrée
    const entryFeeAmount = initial * (entryFee / 100);
    let currentValue = initial - entryFeeAmount;
    let totalContributed = initial;

    // Simulation mensuelle
    for (let month = 1; month <= years * 12; month++) {
        currentValue *= (1 + monthlyReturn - monthlyMgmtFee);
        if (month % 12 === 0) {
            currentValue += monthly * 12;
            totalContributed += monthly * 12;
        }
    }

    const totalFees = entryFeeAmount + (currentValue * (1 - Math.pow(1 - monthlyMgmtFee, years * 12)));
    const totalReturn = currentValue - totalContributed;
    const annualizedReturn = years > 0 ? ((currentValue / totalContributed) ** (1 / years) - 1) * 100 : 0;

    document.getElementById('opcvmTotalInvested').textContent = formatCurrency(totalContributed);
    document.getElementById('opcvmGrossValue').textContent = formatCurrency(currentValue);
    document.getElementById('opcvmNetValue').textContent = formatCurrency(currentValue);
    document.getElementById('opcvmTotalFees').textContent = formatCurrency(totalFees);
    document.getElementById('opcvmTotalReturn').textContent = formatCurrency(totalReturn);
    document.getElementById('opcvmAnnualized').textContent = annualizedReturn.toFixed(1) + '%';
}
