// DONNÉES FISCALITÉ ET RÉGIMES D'ÉPARGNE MAROC - MAI 2026
const fiscaliteData = {
    regimesRetraite: [
        {
            id: "cnss",
            nom: "Régime CNSS",
            type: "Obligatoire",
            description: "Caisse Nationale de Sécurité Sociale. Régime de base pour les salariés du secteur privé.",
            cotisationSalarie: "4.29%",
            cotisationEmployeur: "8.6%",
            plafond: "6000 DH/mois",
            ageDepart: "60 ans (55 pour professions pénibles)",
            avantages: ["Pension de retraite", "Pension d'invalidité", "Pension de veuvage"],
            conditions: "1800 jours de cotisation minimum (5 ans)",
            montantMoyen: "2500-4000 DH/mois"
        },
        {
            id: "cmr",
            nom: "Régime CMR",
            type: "Obligatoire",
            description: "Caisse Marocaine de Retraite pour les fonctionnaires et agents de l'État.",
            cotisationSalarie: "10%",
            cotisationEmployeur: "22%",
            plafond: "Sans plafond",
            ageDepart: "60 ans (55 pour enseignants)",
            avantages: ["Pension calculée sur les 8 derniers salaires", "Revalorisation annuelle", "Pension de réversion"],
            conditions: "15 ans de service minimum",
            montantMoyen: "4000-8000 DH/mois"
        },
        {
            id: "rcar",
            nom: "Régime RCAR",
            type: "Obligatoire",
            description: "Régime Collectif d'Allocation de Retraite pour les collectivités territoriales et établissements publics.",
            cotisationSalarie: "3.75%",
            cotisationEmployeur: "7.5%",
            plafond: "6000 DH/mois",
            ageDepart: "60 ans",
            avantages: ["Pension de retraite", "Capital décès", "Rente d'invalidité"],
            conditions: "1800 jours de cotisation",
            montantMoyen: "2000-3500 DH/mois"
        },
        {
            id: "retraite-complementaire",
            nom: "Retraite Complémentaire (CIMR)",
            type: "Facultatif",
            description: "Caisse Interprofessionnelle Marocaine de Retraite. Épargne retraite complémentaire privée.",
            cotisationSalarie: "Variable (min 200 DH/mois)",
            cotisationEmployeur: "Selon convention",
            plafond: "Sans plafond",
            ageDepart: "55-65 ans (au choix)",
            avantages: ["Déduction fiscale jusqu'à 10% du revenu", "Capital ou rente au choix", "Transmissible aux héritiers"],
            conditions: "Adhésion volontaire",
            montantMoyen: "Selon épargne accumulée"
        }
    ],
    regimesFiscauxEpargne: [
        {
            id: "pea",
            nom: "Plan d'Épargne en Actions (PEA)",
            description: "Encouragement fiscal à l'investissement boursier. Exonération d'IR sur les plus-values après 5 ans de détention.",
            plafond: "800 000 DH",
            avantageFiscal: "Exonération IR sur plus-values après 5 ans",
            conditions: "Résident fiscal marocain, actions cotées à la BVC",
            dureeMin: "5 ans",
            penalite: "15% IR si retrait avant 5 ans"
        },
        {
            id: "pee",
            nom: "Plan d'Épargne Entreprise (PEE)",
            description: "Épargne salariale avec abondement de l'employeur. Exonération IR sur les gains.",
            plafond: "300 000 DH",
            avantageFiscal: "Exonération IR sur intérêts et plus-values",
            conditions: "Salarié d'entreprise proposant le PEE",
            dureeMin: "5 ans",
            penalite: "Perte de l'abondement si retrait avant 5 ans"
        },
        {
            id: "daam-iskane",
            nom: "Daam Iskane (Damane Iskan)",
            description: "Dispositif d'aide à l'accession à la propriété avec garantie de l'État via Tamwilcom.",
            plafond: "800 000 MAD",
            avantageFiscal: "Taux préférentiel 4.50% max, apport 10% min",
            conditions: "Première acquisition, revenus < plafond",
            dureeMax: "25 ans",
            penalite: "Aucune"
        },
        {
            id: "fogarim",
            nom: "Fogarim",
            description: "Fonds de garantie pour les revenus irréguliers. Garantie publique jusqu'à 80% du prêt.",
            plafond: "400 000 MAD",
            avantageFiscal: "Garantie Tamwilcom, apport 0% possible",
            conditions: "Revenus irréguliers (commerçants, artisans)",
            dureeMax: "20 ans",
            penalite: "Aucune"
        },
        {
            id: "fogaloge",
            nom: "Fogaloge Public",
            description: "Dispositif pour les fonctionnaires avec garantie de l'État.",
            plafond: "1 000 000 MAD",
            avantageFiscal: "Taux plafonné 4.50%, apport 10%",
            conditions: "Fonctionnaires et agents de l'État",
            dureeMax: "25 ans",
            penalite: "Aucune"
        },
        {
            id: "epargne-logement",
            nom: "Compte d'Épargne Logement (CEL)",
            description: "Épargne dédiée au logement avec prime d'État.",
            plafond: "500 000 DH",
            avantageFiscal: "Prime d'État 15% (plafond 75 000 DH), exonération IR",
            conditions: "Premier achat immobilier",
            dureeMin: "3 ans",
            penalite: "Perte de la prime"
        },
        {
            id: "assurance-vie",
            nom: "Assurance Vie",
            description: "Contrat d'assurance vie avec avantages fiscaux sur la transmission.",
            plafond: "Sans plafond",
            avantageFiscal: "Exonération droits de succession jusqu'à 500 000 DH par bénéficiaire",
            conditions: "Contrat souscrit auprès d'un assureur agréé",
            dureeMin: "8 ans pour exonération complète",
            penalite: "Imposition des gains si rachat avant 8 ans"
        }
    ],
    impots: {
        is: "20% (taux standard), 15% pour les PME",
        ir: "Progressif de 0% à 38%",
        tva: "20% (standard), 10% (restauration), 7% (transport), 14% (services)"
    }
};
