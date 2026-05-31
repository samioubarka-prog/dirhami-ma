
// ============================================
// DIRHAMI - Données Cartes Bancaires Maroc
// Données basées sur les tarifs des banques marocaines 2026
// ============================================

const cartesBancairesData = [
    {
        id: 'attijari-gold',
        banque: 'Attijariwafa Bank',
        carte: 'Visa Gold',
        type: 'Gold',
        revenuMin: 8000,
        plafondRetrait: 10000,
        plafondPaiement: 50000,
        cotisationAnnuelle: 450,
        retraitDabPropre: 0,
        retraitDabAutre: 8,
        retraitEtranger: 20,
        paiementEtranger: 2.5,
        assuranceVoyage: true,
        assistanceVoyage: true,
        cashback: 0.5,
        programmeFidelite: 'Wafacash',
        avantages: ['Assurance voyage', 'Accès salon VIP', 'Cashback 0.5%'],
        urlOffre: 'https://www.attijariwafabank.com'
    },
    {
        id: 'attijari-platinum',
        banque: 'Attijariwafa Bank',
        carte: 'Visa Platinum',
        type: 'Platinum',
        revenuMin: 15000,
        plafondRetrait: 20000,
        plafondPaiement: 100000,
        cotisationAnnuelle: 900,
        retraitDabPropre: 0,
        retraitDabAutre: 8,
        retraitEtranger: 20,
        paiementEtranger: 2.5,
        assuranceVoyage: true,
        assistanceVoyage: true,
        cashback: 1.0,
        programmeFidelite: 'Wafacash Premium',
        avantages: ['Assurance voyage premium', 'Accès salon VIP monde', 'Cashback 1%', 'Conciergerie'],
        urlOffre: 'https://www.attijariwafabank.com'
    },
    {
        id: 'boa-classic',
        banque: 'Bank of Africa',
        carte: 'Visa Classic',
        type: 'Classic',
        revenuMin: 3000,
        plafondRetrait: 3000,
        plafondPaiement: 15000,
        cotisationAnnuelle: 150,
        retraitDabPropre: 0,
        retraitDabAutre: 7,
        retraitEtranger: 18,
        paiementEtranger: 2.2,
        assuranceVoyage: false,
        assistanceVoyage: false,
        cashback: 0,
        programmeFidelite: 'Aucun',
        avantages: ['Carte internationale', 'Paiement en ligne'],
        urlOffre: 'https://www.bankofafrica.ma'
    },
    {
        id: 'boa-gold',
        banque: 'Bank of Africa',
        carte: 'Visa Gold',
        type: 'Gold',
        revenuMin: 8000,
        plafondRetrait: 10000,
        plafondPaiement: 50000,
        cotisationAnnuelle: 400,
        retraitDabPropre: 0,
        retraitDabAutre: 7,
        retraitEtranger: 18,
        paiementEtranger: 2.2,
        assuranceVoyage: true,
        assistanceVoyage: true,
        cashback: 0.5,
        programmeFidelite: 'BOA Rewards',
        avantages: ['Assurance voyage', 'Cashback 0.5%', 'Offres partenaires'],
        urlOffre: 'https://www.bankofafrica.ma'
    },
    {
        id: 'bp-classic',
        banque: 'Banque Populaire',
        carte: 'Visa Classic',
        type: 'Classic',
        revenuMin: 2500,
        plafondRetrait: 3000,
        plafondPaiement: 15000,
        cotisationAnnuelle: 120,
        retraitDabPropre: 0,
        retraitDabAutre: 6,
        retraitEtranger: 17,
        paiementEtranger: 2.0,
        assuranceVoyage: false,
        assistanceVoyage: false,
        cashback: 0,
        programmeFidelite: 'Aucun',
        avantages: ['Carte internationale', 'Paiement en ligne sécurisé'],
        urlOffre: 'https://www.groupbpce.com'
    },
    {
        id: 'bp-gold',
        banque: 'Banque Populaire',
        carte: 'Visa Gold',
        type: 'Gold',
        revenuMin: 7000,
        plafondRetrait: 10000,
        plafondPaiement: 50000,
        cotisationAnnuelle: 350,
        retraitDabPropre: 0,
        retraitDabAutre: 6,
        retraitEtranger: 17,
        paiementEtranger: 2.0,
        assuranceVoyage: true,
        assistanceVoyage: true,
        cashback: 0.5,
        programmeFidelite: 'BP Rewards',
        avantages: ['Assurance voyage', 'Cashback 0.5%', 'Offres commerçants'],
        urlOffre: 'https://www.groupbpce.com'
    },
    {
        id: 'cih-classic',
        banque: 'CIH Bank',
        carte: 'Visa Classic',
        type: 'Classic',
        revenuMin: 3000,
        plafondRetrait: 3000,
        plafondPaiement: 15000,
        cotisationAnnuelle: 130,
        retraitDabPropre: 0,
        retraitDabAutre: 7,
        retraitEtranger: 18,
        paiementEtranger: 2.2,
        assuranceVoyage: false,
        assistanceVoyage: false,
        cashback: 0,
        programmeFidelite: 'Aucun',
        avantages: ['Carte internationale', 'Paiement en ligne'],
        urlOffre: 'https://www.cihbank.ma'
    },
    {
        id: 'cih-gold',
        banque: 'CIH Bank',
        carte: 'Visa Gold',
        type: 'Gold',
        revenuMin: 8000,
        plafondRetrait: 10000,
        plafondPaiement: 50000,
        cotisationAnnuelle: 380,
        retraitDabPropre: 0,
        retraitDabAutre: 7,
        retraitEtranger: 18,
        paiementEtranger: 2.2,
        assuranceVoyage: true,
        assistanceVoyage: true,
        cashback: 0.5,
        programmeFidelite: 'CIH Rewards',
        avantages: ['Assurance voyage', 'Cashback 0.5%', 'Offres partenaires'],
        urlOffre: 'https://www.cihbank.ma'
    },
    {
        id: 'cdm-classic',
        banque: 'Crédit du Maroc',
        carte: 'Visa Classic',
        type: 'Classic',
        revenuMin: 3000,
        plafondRetrait: 3000,
        plafondPaiement: 15000,
        cotisationAnnuelle: 140,
        retraitDabPropre: 0,
        retraitDabAutre: 7,
        retraitEtranger: 18,
        paiementEtranger: 2.2,
        assuranceVoyage: false,
        assistanceVoyage: false,
        cashback: 0,
        programmeFidelite: 'Aucun',
        avantages: ['Carte internationale', 'Paiement en ligne'],
        urlOffre: 'https://www.creditdumaroc.ma'
    },
    {
        id: 'cdm-gold',
        banque: 'Crédit du Maroc',
        carte: 'Visa Gold',
        type: 'Gold',
        revenuMin: 8000,
        plafondRetrait: 10000,
        plafondPaiement: 50000,
        cotisationAnnuelle: 400,
        retraitDabPropre: 0,
        retraitDabAutre: 7,
        retraitEtranger: 18,
        paiementEtranger: 2.2,
        assuranceVoyage: true,
        assistanceVoyage: true,
        cashback: 0.5,
        programmeFidelite: 'CDM Rewards',
        avantages: ['Assurance voyage', 'Cashback 0.5%'],
        urlOffre: 'https://www.creditdumaroc.ma'
    },
    {
        id: 'sg-classic',
        banque: 'Société Générale Maroc',
        carte: 'Visa Classic',
        type: 'Classic',
        revenuMin: 3000,
        plafondRetrait: 3000,
        plafondPaiement: 15000,
        cotisationAnnuelle: 150,
        retraitDabPropre: 0,
        retraitDabAutre: 7,
        retraitEtranger: 19,
        paiementEtranger: 2.3,
        assuranceVoyage: false,
        assistanceVoyage: false,
        cashback: 0,
        programmeFidelite: 'Aucun',
        avantages: ['Carte internationale', 'Paiement en ligne'],
        urlOffre: 'https://www.societegenerale.ma'
    },
    {
        id: 'sg-gold',
        banque: 'Société Générale Maroc',
        carte: 'Visa Gold',
        type: 'Gold',
        revenuMin: 8000,
        plafondRetrait: 10000,
        plafondPaiement: 50000,
        cotisationAnnuelle: 420,
        retraitDabPropre: 0,
        retraitDabAutre: 7,
        retraitEtranger: 19,
        paiementEtranger: 2.3,
        assuranceVoyage: true,
        assistanceVoyage: true,
        cashback: 0.5,
        programmeFidelite: 'SG Rewards',
        avantages: ['Assurance voyage', 'Cashback 0.5%', 'Offres partenaires'],
        urlOffre: 'https://www.societegenerale.ma'
    },
    {
        id: 'bmce-classic',
        banque: 'BMCE Bank',
        carte: 'Visa Classic',
        type: 'Classic',
        revenuMin: 3000,
        plafondRetrait: 3000,
        plafondPaiement: 15000,
        cotisationAnnuelle: 130,
        retraitDabPropre: 0,
        retraitDabAutre: 7,
        retraitEtranger: 18,
        paiementEtranger: 2.2,
        assuranceVoyage: false,
        assistanceVoyage: false,
        cashback: 0,
        programmeFidelite: 'Aucun',
        avantages: ['Carte internationale', 'Paiement en ligne'],
        urlOffre: 'https://www.bmcebank.ma'
    },
    {
        id: 'bmce-gold',
        banque: 'BMCE Bank',
        carte: 'Visa Gold',
        type: 'Gold',
        revenuMin: 8000,
        plafondRetrait: 10000,
        plafondPaiement: 50000,
        cotisationAnnuelle: 380,
        retraitDabPropre: 0,
        retraitDabAutre: 7,
        retraitEtranger: 18,
        paiementEtranger: 2.2,
        assuranceVoyage: true,
        assistanceVoyage: true,
        cashback: 0.5,
        programmeFidelite: 'BMCE Rewards',
        avantages: ['Assurance voyage', 'Cashback 0.5%'],
        urlOffre: 'https://www.bmcebank.ma'
    },
    {
        id: 'cfg-classic',
        banque: 'CFG Bank',
        carte: 'Visa Classic',
        type: 'Classic',
        revenuMin: 3000,
        plafondRetrait: 3000,
        plafondPaiement: 15000,
        cotisationAnnuelle: 120,
        retraitDabPropre: 0,
        retraitDabAutre: 6,
        retraitEtranger: 17,
        paiementEtranger: 2.0,
        assuranceVoyage: false,
        assistanceVoyage: false,
        cashback: 0,
        programmeFidelite: 'Aucun',
        avantages: ['Carte internationale', 'Paiement en ligne'],
        urlOffre: 'https://www.cfgbank.ma'
    },
    {
        id: 'cfg-gold',
        banque: 'CFG Bank',
        carte: 'Visa Gold',
        type: 'Gold',
        revenuMin: 7000,
        plafondRetrait: 10000,
        plafondPaiement: 50000,
        cotisationAnnuelle: 350,
        retraitDabPropre: 0,
        retraitDabAutre: 6,
        retraitEtranger: 17,
        paiementEtranger: 2.0,
        assuranceVoyage: true,
        assistanceVoyage: true,
        cashback: 0.5,
        programmeFidelite: 'CFG Rewards',
        avantages: ['Assurance voyage', 'Cashback 0.5%'],
        urlOffre: 'https://www.cfgbank.ma'
    },
    {
        id: 'bmci-classic',
        banque: 'BMCI',
        carte: 'Visa Classic',
        type: 'Classic',
        revenuMin: 3000,
        plafondRetrait: 3000,
        plafondPaiement: 15000,
        cotisationAnnuelle: 140,
        retraitDabPropre: 0,
        retraitDabAutre: 7,
        retraitEtranger: 18,
        paiementEtranger: 2.2,
        assuranceVoyage: false,
        assistanceVoyage: false,
        cashback: 0,
        programmeFidelite: 'Aucun',
        avantages: ['Carte internationale', 'Paiement en ligne'],
        urlOffre: 'https://www.bmci.ma'
    },
    {
        id: 'bmci-gold',
        banque: 'BMCI',
        carte: 'Visa Gold',
        type: 'Gold',
        revenuMin: 8000,
        plafondRetrait: 10000,
        plafondPaiement: 50000,
        cotisationAnnuelle: 400,
        retraitDabPropre: 0,
        retraitDabAutre: 7,
        retraitEtranger: 18,
        paiementEtranger: 2.2,
        assuranceVoyage: true,
        assistanceVoyage: true,
        cashback: 0.5,
        programmeFidelite: 'BMCI Rewards',
        avantages: ['Assurance voyage', 'Cashback 0.5%'],
        urlOffre: 'https://www.bmci.ma'
    }
];

// Types de cartes disponibles
const typesCartes = ['Tous', 'Classic', 'Gold', 'Platinum'];

// Banques disponibles
const banquesList = [...new Set(cartesBancairesData.map(c => c.banque))];

// Fonction de filtrage
function filtrerCartes(filters) {
    return cartesBancairesData.filter(carte => {
        if (filters.banque && filters.banque !== 'Toutes' && carte.banque !== filters.banque) return false;
        if (filters.type && filters.type !== 'Tous' && carte.type !== filters.type) return false;
        if (filters.revenuMax && carte.revenuMin > filters.revenuMax) return false;
        if (filters.assuranceVoyage && !carte.assuranceVoyage) return false;
        return true;
    });
}

// Calcul du score de valeur
function calculerScore(carte, usage) {
    let score = 0;

    // Cotisation (moins cher = meilleur)
    score += (1000 - carte.cotisationAnnuelle) / 10;

    // Cashback
    score += carte.cashback * 100;

    // Assurance voyage
    if (carte.assuranceVoyage) score += 20;

    // Frais retrait
    score -= carte.retraitDabAutre * 2;
    score -= carte.retraitEtranger;

    // Frais paiement étranger
    score -= carte.paiementEtranger * 5;

    // Plafonds
    score += carte.plafondPaiement / 5000;

    return Math.round(score);
}

// Calcul des frais estimés annuels
function calculerFraisAnnuels(carte, usage) {
    let total = carte.cotisationAnnuelle;

    // Retraits DAB autres banques
    total += (usage.retraitsAutreBanque || 0) * carte.retraitDabAutre;

    // Retraits à l'étranger
    total += (usage.retraitsEtranger || 0) * carte.retraitEtranger;

    // Paiements à l'étranger
    total += (usage.paiementsEtranger || 0) * (carte.paiementEtranger / 100);

    // Cashback (négatif = économie)
    total -= (usage.paiementsMaroc || 0) * (carte.cashback / 100);

    return Math.round(total);
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { cartesBancairesData, typesCartes, banquesList, filtrerCartes, calculerScore, calculerFraisAnnuels };
}
