// ==================== CARTES BANCAIRES ====================
let allCards = [];
let selectedCards = [];
let comparisonMode = false;

// Charger les cartes au démarrage
document.addEventListener('DOMContentLoaded', loadCards);

async function loadCards() {
    showLoading('cardsGrid');

    try {
        // Charger depuis le fichier JSON local (fallback si API non dispo)
        const response = await fetch('../../backend/app/data/bank_cards.json');
        allCards = await response.json();

        // Remplir les filtres de banques
        const banks = [...new Set(allCards.map(c => c.bank_name))];
        const bankSelect = document.getElementById('filterBank');
        banks.forEach(bank => {
            const option = document.createElement('option');
            option.value = bank;
            option.textContent = bank;
            bankSelect.appendChild(option);
        });

        renderCards(allCards);
    } catch (error) {
        showError('cardsGrid', 'Erreur lors du chargement des cartes bancaires');
    }
}

function renderCards(cards) {
    const grid = document.getElementById('cardsGrid');

    if (cards.length === 0) {
        grid.innerHTML = '<div class="alert alert-info"><i class="fas fa-info-circle"></i> Aucune carte ne correspond à vos critères.</div>';
        return;
    }

    grid.innerHTML = cards.map(card => `
        <div class="bank-card" data-id="${card.id}">
            <div class="bank-card-header">
                <div class="bank-card-logo">${card.bank_name.substring(0, 2).toUpperCase()}</div>
                <div class="bank-card-info">
                    <h3>${card.card_name}</h3>
                    <span class="card-type">${card.bank_name} • ${card.card_type} ${card.card_category || ''}</span>
                </div>
                ${comparisonMode ? `<input type="checkbox" class="compare-checkbox" value="${card.id}" onchange="toggleCardSelection(${card.id})">` : ''}
            </div>
            <div class="bank-card-body">
                <div class="fees-list">
                    <div class="fee-item">
                        <span class="fee-label">Frais annuels</span>
                        <span class="fee-value ${card.annual_fee_mad === 0 ? 'free' : 'paid'}">${card.annual_fee_mad === 0 ? 'Gratuit' : card.annual_fee_mad + ' DH'}</span>
                    </div>
                    <div class="fee-item">
                        <span class="fee-label">Retrait propre DAB</span>
                        <span class="fee-value ${card.withdrawal_fee_own_bank === 0 ? 'free' : 'paid'}">${card.withdrawal_fee_own_bank === 0 ? 'Gratuit' : card.withdrawal_fee_own_bank + ' DH'}</span>
                    </div>
                    <div class="fee-item">
                        <span class="fee-label">Retrait autre DAB</span>
                        <span class="fee-value ${card.withdrawal_fee_other_bank === 0 ? 'free' : 'paid'}">${card.withdrawal_fee_other_bank === 0 ? 'Gratuit' : card.withdrawal_fee_other_bank + ' DH'}</span>
                    </div>
                    <div class="fee-item">
                        <span class="fee-label">Retrait à l'étranger</span>
                        <span class="fee-value">${card.withdrawal_fee_abroad} DH</span>
                    </div>
                    <div class="fee-item">
                        <span class="fee-label">Paiement à l'étranger</span>
                        <span class="fee-value">${card.payment_abroad_fee_percent}%</span>
                    </div>
                </div>
            </div>
            <div class="bank-card-footer">
                <div class="card-tags">
                    ${card.travel_insurance ? '<span class="tag tag-success">Assurance voyage</span>' : ''}
                    ${card.cashback_percent > 0 ? `<span class="tag tag-info">Cashback ${card.cashback_percent}%</span>` : ''}
                    ${card.lounge_access ? '<span class="tag tag-warning">Salon VIP</span>' : ''}
                    ${card.annual_fee_first_year_free ? '<span class="tag tag-success">1ère année gratuite</span>' : ''}
                </div>
            </div>
        </div>
    `).join('');
}

function applyFilters() {
    const bank = document.getElementById('filterBank').value;
    const type = document.getElementById('filterType').value;
    const category = document.getElementById('filterCategory').value;
    const maxFee = document.getElementById('filterMaxFee').value;
    const insurance = document.getElementById('filterInsurance').value;
    const cashback = document.getElementById('filterCashback').value;

    let filtered = allCards;

    if (bank) filtered = filtered.filter(c => c.bank_name === bank);
    if (type) filtered = filtered.filter(c => c.card_type === type);
    if (category) filtered = filtered.filter(c => c.card_category === category);
    if (maxFee) filtered = filtered.filter(c => c.annual_fee_mad <= parseFloat(maxFee));
    if (insurance === 'true') filtered = filtered.filter(c => c.travel_insurance);
    if (insurance === 'false') filtered = filtered.filter(c => !c.travel_insurance);
    if (cashback === 'true') filtered = filtered.filter(c => c.cashback_percent > 0);
    if (cashback === 'false') filtered = filtered.filter(c => c.cashback_percent === 0);

    renderCards(filtered);
}

function resetFilters() {
    document.getElementById('filterBank').value = '';
    document.getElementById('filterType').value = '';
    document.getElementById('filterCategory').value = '';
    document.getElementById('filterMaxFee').value = '';
    document.getElementById('filterInsurance').value = '';
    document.getElementById('filterCashback').value = '';
    renderCards(allCards);
}

function toggleComparisonMode() {
    comparisonMode = !comparisonMode;
    selectedCards = [];
    document.getElementById('comparisonMode').style.display = comparisonMode ? 'block' : 'none';
    document.getElementById('selectedCount').textContent = '0';
    document.getElementById('comparisonTable').style.display = 'none';
    renderCards(allCards);
}

function toggleCardSelection(cardId) {
    const index = selectedCards.indexOf(cardId);
    if (index > -1) {
        selectedCards.splice(index, 1);
    } else {
        if (selectedCards.length < 4) {
            selectedCards.push(cardId);
        } else {
            alert('Vous pouvez comparer maximum 4 cartes');
            document.querySelector(`input[value="${cardId}"]`).checked = false;
            return;
        }
    }
    document.getElementById('selectedCount').textContent = selectedCards.length;
}

function compareSelected() {
    if (selectedCards.length < 2) {
        alert('Sélectionnez au moins 2 cartes pour comparer');
        return;
    }

    const selected = allCards.filter(c => selectedCards.includes(c.id));

    const table = document.getElementById('comparisonTableContent');
    const headers = ['Critère', ...selected.map(c => `${c.bank_name}<br><small>${c.card_name}</small>`)];

    const rows = [
        ['Frais annuels', ...selected.map(c => c.annual_fee_mad === 0 ? 'Gratuit' : c.annual_fee_mad + ' DH')],
        ['1ère année gratuite', ...selected.map(c => c.annual_fee_first_year_free ? 'Oui' : 'Non')],
        ['Retrait propre DAB', ...selected.map(c => c.withdrawal_fee_own_bank === 0 ? 'Gratuit' : c.withdrawal_fee_own_bank + ' DH')],
        ['Retrait autre DAB', ...selected.map(c => c.withdrawal_fee_other_bank === 0 ? 'Gratuit' : c.withdrawal_fee_other_bank + ' DH')],
        ['Retrait à l'étranger', ...selected.map(c => c.withdrawal_fee_abroad + ' DH')],
        ['Paiement à l'étranger', ...selected.map(c => c.payment_abroad_fee_percent + '%')],
        ['Assurance voyage', ...selected.map(c => c.travel_insurance ? '<span style="color:var(--success)">✓ Oui</span>' : '<span style="color:var(--gray-500)">✗ Non</span>')],
        ['Assistance médicale', ...selected.map(c => c.medical_assistance_abroad ? '<span style="color:var(--success)">✓ Oui</span>' : '<span style="color:var(--gray-500)">✗ Non</span>')],
        ['Cashback', ...selected.map(c => c.cashback_percent > 0 ? c.cashback_percent + '%' : 'Non')],
        ['Accès salon VIP', ...selected.map(c => c.lounge_access ? '<span style="color:var(--success)">✓ Oui</span>' : '<span style="color:var(--gray-500)">✗ Non</span>')],
        ['Salaire minimum', ...selected.map(c => c.min_salary_mad + ' DH')],
        ['Programme fidélité', ...selected.map(c => c.loyalty_program || 'Aucun')],
    ];

    table.innerHTML = `
        <thead><tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr></thead>
        <tbody>${rows.map((row, i) => 
            `<tr>${row.map((cell, j) => `<td ${j > 0 && i === 0 ? 'class="highlight"' : ''}>${cell}</td>`).join('')}</tr>`
        ).join('')}</tbody>
    `;

    document.getElementById('comparisonTable').style.display = 'block';
    document.getElementById('comparisonTable').scrollIntoView({ behavior: 'smooth' });
}

function cancelComparison() {
    comparisonMode = false;
    selectedCards = [];
    document.getElementById('comparisonMode').style.display = 'none';
    document.getElementById('comparisonTable').style.display = 'none';
    renderCards(allCards);
}
