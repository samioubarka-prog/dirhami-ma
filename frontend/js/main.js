// ============================================
// Dirhami.ma - Main JavaScript
// Frontend complet avec simulateurs, API, UI
// ============================================

const API_BASE = window.location.origin.includes('localhost') ? 'http://localhost:5000/api' : '/api';

// ===== UTILITAIRES =====
function formatMAD(n) {
    return new Intl.NumberFormat('fr-MA', { style: 'currency', currency: 'MAD', maximumFractionDigits: 0 }).format(n);
}

function formatNumber(n) {
    return new Intl.NumberFormat('fr-MA').format(n);
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : 'exclamation-circle';
    toast.innerHTML = `<i class="fas fa-${icon}"></i> <span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

function toggleSpinner(btnId, spinnerId, textId, show) {
    const spinner = document.getElementById(spinnerId);
    const text = document.getElementById(textId);
    const btn = document.getElementById(btnId);
    if (spinner) spinner.style.display = show ? 'inline-block' : 'none';
    if (text) text.style.display = show ? 'none' : 'inline';
    if (btn) btn.disabled = show;
}

// ===== NAVIGATION =====
function initNav() {
    const navbar = document.getElementById('navbar');
    const mobileBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');

    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        });
    }

    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }
}

// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}

// ===== POPUP EMAIL (style tamra.ma) =====
function initPopupEmail() {
    const popup = document.getElementById('popupEmail');
    const closeBtn = document.getElementById('popupClose');
    const form = document.getElementById('popupForm');

    if (!popup) return;

    let shown = false;
    const showPopup = () => {
        if (!shown && !localStorage.getItem('popupClosed')) {
            popup.classList.add('active');
            shown = true;
        }
    };

    setTimeout(showPopup, 15000);
    window.addEventListener('scroll', () => {
        if ((window.scrollY + window.innerHeight) / document.body.scrollHeight > 0.5) {
            showPopup();
        }
    }, { once: true });

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            popup.classList.remove('active');
            localStorage.setItem('popupClosed', 'true');
        });
    }

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('popupEmailInput').value;
            try {
                const res = await fetch(`${API_BASE}/leads`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, source: 'popup' })
                });
                if (res.ok) {
                    showToast('Inscription réussie ! Merci.');
                    popup.classList.remove('active');
                } else {
                    showToast('Cet email est déjà inscrit.', 'warning');
                }
            } catch (err) {
                showToast('Erreur de connexion.', 'error');
            }
        });
    }
}

// ===== LEADS / COLLECTE EMAIL =====
function initLeadForms() {
    const leadForm = document.getElementById('leadForm');
    if (leadForm) {
        leadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            toggleSpinner('leadForm', 'leadSpinner', 'leadBtnText', true);

            const data = {
                email: document.getElementById('leadEmail').value,
                nom: document.getElementById('leadNom').value,
                telephone: document.getElementById('leadPhone').value,
                objet: document.getElementById('leadObjet').value,
                source: 'homepage'
            };

            try {
                const res = await fetch(`${API_BASE}/leads`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (res.ok) {
                    showToast('✅ Guide envoyé ! Consultez votre email.');
                    leadForm.reset();
                } else {
                    showToast('Cet email est déjà inscrit.', 'warning');
                }
            } catch (err) {
                showToast('Erreur serveur. Veuillez réessayer.', 'error');
            } finally {
                toggleSpinner('leadForm', 'leadSpinner', 'leadBtnText', false);
            }
        });
    }

    const ctaForm = document.getElementById('ctaForm');
    if (ctaForm) {
        ctaForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('ctaEmail').value;
            try {
                const res = await fetch(`${API_BASE}/leads`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, source: 'cta_section' })
                });
                if (res.ok) {
                    showToast('Inscription aux alertes réussie !');
                    ctaForm.reset();
                } else {
                    showToast('Email déjà inscrit.', 'warning');
                }
            } catch (err) {
                showToast('Erreur de connexion.', 'error');
            }
        });
    }
}

// ===== SIMULATEUR CRÉDIT =====
function initSimulateurCredit() {
    const btn = document.getElementById('btnCalculerCredit');
    if (!btn) return;

    const montantInput = document.getElementById('creditMontant');
    const montantRange = document.getElementById('creditMontantRange');
    const apportInput = document.getElementById('creditApport');
    const apportRange = document.getElementById('creditApportRange');

    if (montantInput && montantRange) {
        montantInput.addEventListener('input', () => montantRange.value = montantInput.value);
        montantRange.addEventListener('input', () => montantInput.value = montantRange.value);
    }
    if (apportInput && apportRange) {
        apportInput.addEventListener('input', () => apportRange.value = apportInput.value);
        apportRange.addEventListener('input', () => apportInput.value = apportRange.value);
    }

    btn.addEventListener('click', async () => {
        const montant = parseFloat(document.getElementById('creditMontant').value) || 0;
        const apport = parseFloat(document.getElementById('creditApport').value) || 0;
        const taux = parseFloat(document.getElementById('creditTaux').value) || 6.5;
        const duree = parseInt(document.getElementById('creditDuree').value) || 20;
        const revenu = parseFloat(document.getElementById('creditRevenu').value) || 15000;

        if (montant <= 0 || duree <= 0) {
            showToast('Veuillez remplir tous les champs correctement.', 'error');
            return;
        }

        const capital = montant - apport;
        const n = duree * 12;
        const tauxM = taux / 100 / 12;
        let mensualite = 0;
        if (tauxM > 0) {
            mensualite = capital * (tauxM * Math.pow(1 + tauxM, n)) / (Math.pow(1 + tauxM, n) - 1);
        } else {
            mensualite = capital / n;
        }
        const coutTotal = mensualite * n;
        const interets = coutTotal - capital;
        const endettement = (mensualite / revenu) * 100;

        document.getElementById('resMensualite').textContent = formatMAD(mensualite);
        document.getElementById('resCoutTotal').textContent = formatMAD(coutTotal);
        document.getElementById('resInterets').textContent = formatMAD(interets);
        document.getElementById('resEndettement').textContent = endettement.toFixed(1) + '%';

        const boxEndettement = document.getElementById('boxEndettement');
        const valEndettement = document.getElementById('resEndettement');
        if (endettement > 40) {
            boxEndettement.classList.add('danger');
            valEndettement.classList.add('danger');
            showToast('⚠️ Taux d'endettement > 40%. Les banques risquent de refuser.', 'warning');
        } else {
            boxEndettement.classList.remove('danger');
            valEndettement.classList.remove('danger');
        }

        document.getElementById('creditResults').style.display = 'block';

        const ctx = document.getElementById('creditChart');
        if (ctx) {
            if (window.creditChartInstance) window.creditChartInstance.destroy();
            window.creditChartInstance = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Capital emprunté', 'Intérêts'],
                    datasets: [{
                        data: [capital, interets],
                        backgroundColor: ['#0f2b46', '#fdcb6e'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' },
                        title: { display: true, text: 'Répartition du coût total' }
                    }
                }
            });
        }

        const tbody = document.querySelector('#tableAmortissement tbody');
        if (tbody) {
            tbody.innerHTML = '';
            let solde = capital;
            for (let i = 1; i <= Math.min(n, 12); i++) {
                const interetMois = solde * tauxM;
                const amort = mensualite - interetMois;
                solde -= amort;
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${i}</td>
                    <td>${formatMAD(mensualite)}</td>
                    <td>${formatMAD(interetMois)}</td>
                    <td>${formatMAD(amort)}</td>
                    <td>${formatMAD(Math.max(solde, 0))}</td>
                `;
                tbody.appendChild(tr);
            }
        }

        try {
            await fetch(`${API_BASE}/simulations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    type: 'credit',
                    params: { montant, apport, taux, duree, revenu },
                    resultats: { mensualite, coutTotal, interets, endettement }
                })
            });
        } catch (e) {}
    });

    const btnTableau = document.getElementById('btnTableau');
    if (btnTableau) {
        btnTableau.addEventListener('click', () => {
            const div = document.getElementById('tableauAmortissement');
            div.style.display = div.style.display === 'none' ? 'block' : 'none';
            btnTableau.innerHTML = div.style.display === 'none' 
                ? '<i class="fas fa-table"></i> Voir le tableau d'amortissement'
                : '<i class="fas fa-eye-slash"></i> Masquer le tableau';
        });
    }
}

// ===== SIMULATEUR RETRAITE =====
function initSimulateurRetraite() {
    const btn = document.getElementById('btnCalculerRetraite');
    if (!btn) return;

    const tauxRange = document.getElementById('retTaux');
    const tauxVal = document.getElementById('retTauxVal');
    const rendRange = document.getElementById('retRendement');
    const rendVal = document.getElementById('retRendementVal');

    if (tauxRange && tauxVal) {
        tauxRange.addEventListener('input', () => tauxVal.textContent = tauxRange.value + '%');
    }
    if (rendRange && rendVal) {
        rendRange.addEventListener('input', () => rendVal.textContent = rendRange.value + '%');
    }

    btn.addEventListener('click', async () => {
        const ageActuel = parseInt(document.getElementById('retAgeActuel').value) || 35;
        const ageRetraite = parseInt(document.getElementById('retAgeDepart').value) || 60;
        const revenu = parseFloat(document.getElementById('retRevenu').value) || 12000;
        const tauxRemplacement = parseFloat(document.getElementById('retTaux').value) || 70;
        const rendement = parseFloat(document.getElementById('retRendement').value) || 6;
        const capitalExistant = parseFloat(document.getElementById('retCapital').value) || 0;

        const annees = ageRetraite - ageActuel;
        const besoinMensuel = revenu * (tauxRemplacement / 100);
        const besoinAnnuel = besoinMensuel * 12;
        const rendementDecimal = rendement / 100;

        const capitalNecessaire = besoinAnnuel / rendementDecimal;
        const capitalAConstituer = Math.max(capitalNecessaire - capitalExistant, 0);
        const n = annees * 12;
        const tauxM = rendementDecimal / 12;
        let versementMensuel = 0;
        if (tauxM > 0 && n > 0) {
            versementMensuel = capitalAConstituer * tauxM / (Math.pow(1 + tauxM, n) - 1);
        } else if (n > 0) {
            versementMensuel = capitalAConstituer / n;
        }

        let capitalProjete = capitalExistant;
        const evolution = [];
        for (let a = 0; a <= annees; a++) {
            if (a > 0) {
                capitalProjete = (capitalProjete + versementMensuel * 12) * (1 + rendementDecimal);
            }
            evolution.push({ annee: ageActuel + a, capital: Math.round(capitalProjete) });
        }

        document.getElementById('resCapitalNec').textContent = formatMAD(capitalNecessaire);
        document.getElementById('resVersement').textContent = formatMAD(versementMensuel);
        document.getElementById('resBesoin').textContent = formatMAD(besoinMensuel);
        document.getElementById('resAnnees').textContent = annees + ' ans';
        document.getElementById('resProjete').textContent = formatMAD(capitalProjete);
        document.getElementById('retResults').style.display = 'block';

        const ctx = document.getElementById('retChart');
        if (ctx) {
            if (window.retChartInstance) window.retChartInstance.destroy();
            window.retChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: evolution.map(e => e.annee + ' ans'),
                    datasets: [{
                        label: 'Capital projeté',
                        data: evolution.map(e => e.capital),
                        borderColor: '#00b894',
                        backgroundColor: 'rgba(0,184,148,0.1)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 4,
                        pointBackgroundColor: '#00b894'
                    }, {
                        label: 'Capital nécessaire',
                        data: evolution.map(() => capitalNecessaire),
                        borderColor: '#fdcb6e',
                        borderDash: [5, 5],
                        fill: false,
                        pointRadius: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' },
                        title: { display: true, text: 'Évolution de votre épargne retraite' }
                    },
                    scales: {
                        y: { ticks: { callback: v => formatMAD(v) } }
                    }
                }
            });
        }

        try {
            await fetch(`${API_BASE}/simulations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    type: 'retraite',
                    params: { ageActuel, ageRetraite, revenu, tauxRemplacement, rendement },
                    resultats: { capitalNecessaire, versementMensuel, capitalProjete }
                })
            });
        } catch (e) {}
    });
}

// ===== SIMULATEUR INVESTISSEMENT =====
function initSimulateurInvestissement() {
    const btn = document.getElementById('btnCalculerInvest');
    if (!btn) return;

    const rendRange = document.getElementById('invRendement');
    const rendVal = document.getElementById('invRendementVal');
    const dureeRange = document.getElementById('invDuree');
    const dureeVal = document.getElementById('invDureeVal');

    if (rendRange && rendVal) rendRange.addEventListener('input', () => rendVal.textContent = rendRange.value + '%');
    if (dureeRange && dureeVal) dureeRange.addEventListener('input', () => dureeVal.textContent = dureeRange.value + ' ans');

    btn.addEventListener('click', async () => {
        const capitalInitial = parseFloat(document.getElementById('invCapital').value) || 0;
        const versementMensuel = parseFloat(document.getElementById('invVersement').value) || 0;
        const rendement = parseFloat(document.getElementById('invRendement').value) || 7;
        const duree = parseInt(document.getElementById('invDuree').value) || 10;

        const r = rendement / 100;
        const tauxM = r / 12;
        const n = duree * 12;

        const vfCapital = capitalInitial * Math.pow(1 + r, duree);
        const vfVersements = tauxM > 0 
            ? versementMensuel * (Math.pow(1 + tauxM, n) - 1) / tauxM 
            : versementMensuel * n;
        const total = vfCapital + vfVersements;
        const capitalInvesti = capitalInitial + (versementMensuel * n);
        const interets = total - capitalInvesti;
        const performance = capitalInvesti > 0 ? ((interets / capitalInvesti) * 100) : 0;

        const evolution = [];
        let capital = capitalInitial;
        for (let a = 0; a <= duree; a++) {
            if (a > 0) capital = capital * (1 + r) + versementMensuel * 12;
            evolution.push({ annee: a, capital: Math.round(capital) });
        }

        document.getElementById('resTotal').textContent = formatMAD(total);
        document.getElementById('resInterets').textContent = formatMAD(interets);
        document.getElementById('resCapitalInvesti').textContent = formatMAD(capitalInvesti);
        document.getElementById('resPerformance').textContent = '+' + performance.toFixed(1) + '%';
        document.getElementById('invResults').style.display = 'block';

        const ctx = document.getElementById('invChart');
        if (ctx) {
            if (window.invChartInstance) window.invChartInstance.destroy();
            window.invChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: evolution.map(e => 'An ' + e.annee),
                    datasets: [{
                        label: 'Capital cumulé',
                        data: evolution.map(e => e.capital),
                        backgroundColor: '#0f2b46',
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' },
                        title: { display: true, text: 'Projection de capital sur ' + duree + ' ans' }
                    },
                    scales: {
                        y: { ticks: { callback: v => formatMAD(v) } }
                    }
                }
            });
        }

        try {
            await fetch(`${API_BASE}/simulations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    type: 'investissement',
                    params: { capitalInitial, versementMensuel, rendement, duree },
                    resultats: { total, interets, performance }
                })
            });
        } catch (e) {}
    });
}

// ===== SIMULATEUR BUDGET =====
function initSimulateurBudget() {
    const btn = document.getElementById('btnCalculerBudget');
    if (!btn) return;

    const objRange = document.getElementById('budObjectif');
    const objVal = document.getElementById('budObjectifVal');
    if (objRange && objVal) objRange.addEventListener('input', () => objVal.textContent = objRange.value + '%');

    btn.addEventListener('click', async () => {
        const revenus = parseFloat(document.getElementById('budRevenus').value) || 0;
        const loyer = parseFloat(document.getElementById('budLoyer').value) || 0;
        const transport = parseFloat(document.getElementById('budTransport').value) || 0;
        const nourriture = parseFloat(document.getElementById('budNourriture').value) || 0;
        const sante = parseFloat(document.getElementById('budSante').value) || 0;
        const loisirs = parseFloat(document.getElementById('budLoisirs').value) || 0;
        const autres = parseFloat(document.getElementById('budAutres').value) || 0;
        const objectif = parseFloat(document.getElementById('budObjectif').value) || 20;

        const totalDepenses = loyer + transport + nourriture + sante + loisirs + autres;
        const solde = revenus - totalDepenses;
        const epargneRec = revenus * (objectif / 100);
        const tauxEpargne = revenus > 0 ? (solde / revenus) * 100 : 0;
        const tauxEndettement = revenus > 0 ? (totalDepenses / revenus) * 100 : 0;

        document.getElementById('resSolde').textContent = formatMAD(solde);
        document.getElementById('resDepenses').textContent = formatMAD(totalDepenses);
        document.getElementById('resTauxEpargne').textContent = tauxEpargne.toFixed(1) + '%';
        document.getElementById('resEndettementBud').textContent = tauxEndettement.toFixed(1) + '%';
        document.getElementById('resEpargneRec').textContent = formatMAD(epargneRec);
        document.getElementById('budResults').style.display = 'block';

        const suggestionsDiv = document.getElementById('suggestionsBudget');
        suggestionsDiv.innerHTML = '';
        const suggestions = [];
        if (loyer > revenus * 0.33) suggestions.push({ text: '🏠 Votre loyer dépasse 33% de vos revenus. Envisagez un logement moins cher.', type: 'warning' });
        if (transport > revenus * 0.15) suggestions.push({ text: '🚗 Vos frais de transport sont élevés. Essayez le covoiturage ou bus.', type: 'warning' });
        if (loisirs > revenus * 0.1) suggestions.push({ text: '🎉 Vos loisirs dépassent 10%. Réduisez les sorties ou choisissez des activités gratuites.', type: 'warning' });
        if (nourriture > revenus * 0.2) suggestions.push({ text: '🍽️ Votre budget nourriture est élevé. Faites vos courses en gros et cuisinez chez vous.', type: 'warning' });
        if (solde < 0) suggestions.push({ text: '⚠️ Vous êtes en déficit ! Réduisez immédiatement vos dépenses.', type: 'danger' });
        else if (solde < epargneRec) suggestions.push({ text: `💡 Il vous manque ${Math.round(epargneRec - solde)} MAD/mois pour atteindre votre objectif d'épargne de ${objectif}%.`, type: '' });
        else suggestions.push({ text: `✅ Bravo ! Vous épargnez ${Math.round(solde)} MAD/mois, ce qui dépasse votre objectif.`, type: 'success' });

        suggestions.forEach(s => {
            const div = document.createElement('div');
            div.className = 'suggestion-box' + (s.type ? ' ' + s.type : '');
            div.innerHTML = `<p style="margin:0; font-size:0.95rem; line-height:1.6;">${s.text}</p>`;
            suggestionsDiv.appendChild(div);
        });

        const ctx = document.getElementById('budChart');
        if (ctx) {
            if (window.budChartInstance) window.budChartInstance.destroy();
            window.budChartInstance = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Loyer', 'Transport', 'Nourriture', 'Santé', 'Loisirs', 'Autres', 'Épargne'],
                    datasets: [{
                        data: [loyer, transport, nourriture, sante, loisirs, autres, Math.max(solde, 0)],
                        backgroundColor: ['#d63031', '#e17055', '#00b894', '#0984e3', '#6c5ce7', '#b2bec3', '#0f2b46'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' },
                        title: { display: true, text: 'Répartition de votre budget' }
                    }
                }
            });
        }

        try {
            await fetch(`${API_BASE}/simulations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    type: 'budget',
                    params: { revenus, loyer, transport, nourriture, sante, loisirs, autres, objectif },
                    resultats: { totalDepenses, solde, tauxEpargne }
                })
            });
        } catch (e) {}
    });
}

// ===== COMPARATEUR CARTES =====
async function initComparateurCartes() {
    const tableBody = document.querySelector('#tableCartes tbody');
    const filtreBanque = document.getElementById('filtreBanque');
    const filtreType = document.getElementById('filtreType');
    const btnFiltrer = document.getElementById('btnFiltrerCartes');
    if (!tableBody) return;

    let allCartes = [];
    try {
        const res = await fetch(`${API_BASE}/cartes`);
        allCartes = await res.json();
    } catch (e) {
        showToast('Erreur de chargement des données.', 'error');
        return;
    }

    const banques = [...new Set(allCartes.map(c => c.banque))];
    banques.forEach(b => {
        const opt = document.createElement('option');
        opt.value = b;
        opt.textContent = b;
        filtreBanque.appendChild(opt);
    });

    function renderCartes(cartes) {
        tableBody.innerHTML = '';
        cartes.forEach(c => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${c.banque}</strong></td>
                <td>${c.nom_carte}</td>
                <td><span class="badge badge-info">${c.type}</span></td>
                <td>${c.frais_annuels} MAD</td>
                <td>${c.retrait_dab_national} MAD</td>
                <td>${c.retrait_dab_international} MAD</td>
                <td>${formatNumber(c.plafond_retrait_jour)}</td>
                <td>${formatNumber(c.plafond_paiement_jour)}</td>
                <td>${formatNumber(c.plafond_internet)}</td>
                <td>${c.assurance_voyage ? '<i class="fas fa-check" style="color:#00b894"></i>' : '<i class="fas fa-times" style="color:#b2bec3"></i>'}</td>
                <td>${c.cashback > 0 ? c.cashback + '%' : '-'}</td>
                <td>${c.avantages}</td>
            `;
            tableBody.appendChild(tr);
        });
    }

    renderCartes(allCartes);

    if (btnFiltrer) {
        btnFiltrer.addEventListener('click', () => {
            const b = filtreBanque.value;
            const t = filtreType.value;
            let filtered = allCartes;
            if (b) filtered = filtered.filter(c => c.banque === b);
            if (t) filtered = filtered.filter(c => c.type === t);
            renderCartes(filtered);
        });
    }
}

// ===== COMPARATEUR OPCVM =====
async function initComparateurOPCVM() {
    const tableBody = document.querySelector('#tableOPCVM tbody');
    const filtreCat = document.getElementById('filtreCategorie');
    const btnFiltrer = document.getElementById('btnFiltrerOPCVM');
    if (!tableBody) return;

    let allOPCVM = [];
    try {
        const res = await fetch(`${API_BASE}/opcvm`);
        allOPCVM = await res.json();
    } catch (e) {
        showToast('Erreur de chargement des OPCVM.', 'error');
        return;
    }

    function renderOPCVM(data) {
        tableBody.innerHTML = '';
        data.forEach(o => {
            const tr = document.createElement('tr');
            const risqueClass = o.risque === 'Faible' || o.risque === 'Très faible' ? 'badge-success' : 
                               o.risque === 'Moyen' ? 'badge-warning' : 'badge-danger';
            tr.innerHTML = `
                <td><strong>${o.nom}</strong><br><small style="color:var(--gray)">${o.description || ''}</small></td>
                <td><span class="badge ${risqueClass}">${o.categorie}</span></td>
                <td>${o.societe}</td>
                <td style="color:${o.rendement_1an >= 0 ? '#00b894' : '#d63031'}; font-weight:600">${o.rendement_1an}%</td>
                <td style="color:${o.rendement_3ans >= 0 ? '#00b894' : '#d63031'}; font-weight:600">${o.rendement_3ans}%</td>
                <td>${o.frais_gestion}%</td>
                <td><span class="badge ${risqueClass}">${o.risque}</span></td>
                <td>${formatNumber(o.min_investissement)} MAD</td>
                <td>${formatNumber(o.actif_total)}</td>
            `;
            tableBody.appendChild(tr);
        });
    }

    renderOPCVM(allOPCVM);

    if (btnFiltrer) {
        btnFiltrer.addEventListener('click', () => {
            const cat = filtreCat.value;
            renderOPCVM(cat ? allOPCVM.filter(o => o.categorie === cat) : allOPCVM);
        });
    }

    const ctx = document.getElementById('opcvmChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: allOPCVM.map(o => o.nom.split(' ').slice(0, 2).join(' ')),
                datasets: [{
                    label: 'Rendement 1 an (%)',
                    data: allOPCVM.map(o => o.rendement_1an),
                    backgroundColor: allOPCVM.map(o => o.rendement_1an >= 0 ? '#00b894' : '#d63031'),
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' },
                    title: { display: true, text: 'Rendements 1 an des OPCVM' }
                }
            }
        });
    }
}

// ===== BLOG =====
async function initBlog() {
    const grid = document.getElementById('blogGrid');
    const preview = document.getElementById('blogPreview');
    const filtre = document.getElementById('filtreBlog');
    const articleContent = document.getElementById('articleContent');

    if (articleContent) {
        const slug = new URLSearchParams(window.location.search).get('slug');
        if (slug) {
            try {
                const res = await fetch(`${API_BASE}/articles/${slug}`);
                const article = await res.json();
                if (article.error) {
                    articleContent.innerHTML = '<p>Article non trouvé.</p>';
                    return;
                }
                articleContent.innerHTML = `
                    <div class="blog-category">${article.categorie}</div>
                    <h1>${article.titre}</h1>
                    <div class="blog-meta" style="margin-bottom: 2rem;">
                        <span><i class="fas fa-calendar"></i> ${new Date(article.date_pub).toLocaleDateString('fr-MA')}</span>
                        <span><i class="fas fa-eye"></i> ${article.lu} lectures</span>
                    </div>
                    <div style="line-height: 1.8; color: var(--dark);">
                        ${article.contenu}
                    </div>
                    <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--gray-light);">
                        <a href="blog.html" class="btn btn-secondary btn-sm"><i class="fas fa-arrow-left"></i> Retour au blog</a>
                    </div>
                `;
            } catch (e) {
                articleContent.innerHTML = '<p>Erreur de chargement.</p>';
            }
        }
        return;
    }

    let allArticles = [];
    try {
        const res = await fetch(`${API_BASE}/articles`);
        allArticles = await res.json();
    } catch (e) { return; }

    function renderArticles(articles, container, limit = null) {
        container.innerHTML = '';
        const toShow = limit ? articles.slice(0, limit) : articles;
        toShow.forEach(a => {
            const card = document.createElement('div');
            card.className = 'blog-card';
            card.innerHTML = `
                <div class="blog-image"><i class="fas fa-newspaper"></i></div>
                <div class="blog-content">
                    <div class="blog-category">${a.categorie}</div>
                    <h3>${a.titre}</h3>
                    <p>${a.contenu.replace(/<[^>]*>/g, '').substring(0, 120)}...</p>
                    <div class="blog-meta">
                        <span>${new Date(a.date_pub).toLocaleDateString('fr-MA')}</span>
                        <a href="article.html?slug=${a.slug}">Lire <i class="fas fa-arrow-right"></i></a>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    }

    if (grid) renderArticles(allArticles, grid);
    if (preview) renderArticles(allArticles, preview, 3);

    if (filtre) {
        filtre.addEventListener('change', () => {
            const cat = filtre.value;
            renderArticles(cat ? allArticles.filter(a => a.categorie === cat) : allArticles, grid);
        });
    }
}

// ===== ADMIN =====
async function initAdmin() {
    const statLeads = document.getElementById('statLeads');
    if (!statLeads) return;

    try {
        const statsRes = await fetch(`${API_BASE}/stats`);
        const stats = await statsRes.json();
        document.getElementById('statLeads').textContent = stats.total_leads;
        document.getElementById('statLeadsToday').textContent = stats.leads_today;
        document.getElementById('statSimulations').textContent = stats.total_simulations;
        document.getElementById('statArticles').textContent = stats.total_articles;
    } catch (e) {}

    try {
        const leadsRes = await fetch(`${API_BASE}/leads`);
        const leads = await leadsRes.json();
        const tbody = document.querySelector('#tableLeads tbody');
        if (tbody) {
            tbody.innerHTML = '';
            leads.forEach(l => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${new Date(l.date_inscription).toLocaleDateString('fr-MA')}</td>
                    <td>${l.nom || '-'}</td>
                    <td><a href="mailto:${l.email}" style="color:var(--primary)">${l.email}</a></td>
                    <td>${l.telephone || '-'}</td>
                    <td><span class="badge badge-success">${l.objet || '-'}</span></td>
                    <td>${l.source}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        const btnExportLeads = document.getElementById('btnExportLeads');
        if (btnExportLeads) {
            btnExportLeads.addEventListener('click', () => {
                const csv = [
                    ['Date', 'Nom', 'Email', 'Téléphone', 'Intérêt', 'Source'],
                    ...leads.map(l => [
                        l.date_inscription, l.nom || '', l.email, l.telephone || '', l.objet || '', l.source
                    ])
                ].map(row => row.map(c => `"${c}"`).join(',')).join('\n');
                const blob = new Blob([csv], { type: 'text/csv' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'leads_dirhami_' + new Date().toISOString().split('T')[0] + '.csv';
                a.click();
                showToast('Export CSV des leads réussi !');
            });
        }
    } catch (e) {}
}

// ===== INITIALISATION =====
document.addEventListener('DOMContentLoaded', () => {
    initNav();
    initScrollAnimations();
    initPopupEmail();
    initLeadForms();
    initSimulateurCredit();
    initSimulateurRetraite();
    initSimulateurInvestissement();
    initSimulateurBudget();
    initComparateurCartes();
    initComparateurOPCVM();
    initBlog();
    initAdmin();
});
