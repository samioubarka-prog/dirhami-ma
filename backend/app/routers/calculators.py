from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from math import pow

router = APIRouter(prefix="/calculators", tags=["calculators"])

# --- Credit Immobilier ---
class CreditInput(BaseModel):
    prix_bien: float
    apport: float
    taux_annuel: float
    duree_annees: int
    type_credit: str = "classique"
    taux_assurance: float = 0.36
    frais_dossier_pct: float = 1.0

class CreditOutput(BaseModel):
    montant_emprunt: float
    mensualite_hors_assurance: float
    mensualite_avec_assurance: float
    cout_total_interets: float
    cout_total_assurance: float
    cout_global: float
    teg: float
    revenu_necessaire: float
    tableau_amortissement: list

@router.post("/credit", response_model=CreditOutput)
def calculate_credit(data: CreditInput):
    montant = max(0, data.prix_bien - data.apport)
    duree_mois = data.duree_annees * 12
    taux_mensuel = data.taux_annuel / 100 / 12
    taux_assurance_mensuel = data.taux_assurance / 100 / 12

    mensualite = 0
    tableau = []

    if data.type_credit == "classique":
        if taux_mensuel > 0:
            mensualite = montant * (taux_mensuel * pow(1 + taux_mensuel, duree_mois)) / (pow(1 + taux_mensuel, duree_mois) - 1)
        else:
            mensualite = montant / duree_mois

        capital_restant = montant
        total_interets = 0
        for mois in range(1, duree_mois + 1):
            interets = capital_restant * taux_mensuel
            assurance_mois = capital_restant * taux_assurance_mensuel
            amortissement = mensualite - interets
            capital_restant -= amortissement
            if capital_restant < 0:
                capital_restant = 0
            total_interets += interets
            tableau.append({
                "mois": mois,
                "mensualite": round(mensualite + assurance_mois, 2),
                "interets": round(interets, 2),
                "amortissement": round(amortissement, 2),
                "assurance": round(assurance_mois, 2),
                "capital_restant": round(capital_restant, 2)
            })
        cout_interets = total_interets
    else:
        interets_mensuels = montant * taux_mensuel
        mensualite = interets_mensuels
        assurance_mois = montant * taux_assurance_mensuel
        for mois in range(1, duree_mois + 1):
            tableau.append({
                "mois": mois,
                "mensualite": round(interets_mensuels + assurance_mois, 2),
                "interets": round(interets_mensuels, 2),
                "amortissement": montant if mois == duree_mois else 0,
                "assurance": round(assurance_mois, 2),
                "capital_restant": 0 if mois == duree_mois else montant
            })
        cout_interets = interets_mensuels * duree_mois

    assurance_totale = sum(l["assurance"] for l in tableau)
    frais_dossier = montant * data.frais_dossier_pct / 100
    cout_global = montant + cout_interets + assurance_totale + frais_dossier
    teg = ((cout_global - montant) / montant * 100 / data.duree_annees) if montant > 0 else 0
    revenu_necessaire = (mensualite * 1.4) / 0.4

    return {
        "montant_emprunt": montant,
        "mensualite_hors_assurance": round(mensualite, 2),
        "mensualite_avec_assurance": round(mensualite + tableau[0]["assurance"], 2),
        "cout_total_interets": round(cout_interets, 2),
        "cout_total_assurance": round(assurance_totale, 2),
        "cout_global": round(cout_global, 2),
        "teg": round(teg, 2),
        "revenu_necessaire": round(revenu_necessaire, 2),
        "tableau_amortissement": tableau[:12] + ([tableau[-1]] if duree_mois > 12 else [])
    }

# --- Retraite ---
class RetraiteInput(BaseModel):
    age_actuel: int
    age_retraite: int
    salaire: float
    regime: str
    annees_cotisees: int
    epargne_actuelle: float
    versement_mensuel: float
    rendement: float

@router.post("/retraite")
def calculate_retraite(data: RetraiteInput):
    annees_restantes = data.age_retraite - data.age_actuel
    annees_totales = data.annees_cotisees + annees_restantes

    pension = 0
    if data.regime == "cnss":
        salaire_plafonne = min(data.salaire, 6000)
        taux = min(50 + max(0, annees_totales - 9) * 2, 70)
        pension = salaire_plafonne * (taux / 100)
    elif data.regime == "cmr":
        taux = min(annees_totales * 2.5, 100)
        pension = data.salaire * (taux / 100)
    elif data.regime == "rcar":
        salaire_plafonne = min(data.salaire, 6000)
        taux = min(50 + max(0, annees_totales - 9) * 2, 70)
        pension = salaire_plafonne * (taux / 100)

    pension = max(pension, 1000)

    taux_mensuel = data.rendement / 100 / 12
    nb_mois = annees_restantes * 12
    valeur_epargne = data.epargne_actuelle * pow(1 + taux_mensuel, nb_mois) + data.versement_mensuel * (pow(1 + taux_mensuel, nb_mois) - 1) / taux_mensuel
    rente_mensuelle = valeur_epargne * 0.04 / 12

    return {
        "pension_base": round(pension, 2),
        "rente_complementaire": round(rente_mensuelle, 2),
        "revenu_total": round(pension + rente_mensuelle, 2),
        "capital_epargne": round(valeur_epargne, 2),
        "taux_remplacement": round((pension + rente_mensuelle) / data.salaire * 100, 1),
        "besoin_estime": round(data.salaire * 0.7, 2),
        "ecart": round(data.salaire * 0.7 - pension - rente_mensuelle, 2)
    }

# --- Budget ---
class BudgetInput(BaseModel):
    revenu: float
    loyer: float
    charges: float
    courses: float
    transport: float
    telephone: float
    sante: float
    loisirs: float
    shopping: float
    autres: float

@router.post("/budget")
def calculate_budget(data: BudgetInput):
    total = data.loyer + data.charges + data.courses + data.transport + data.telephone + data.sante + data.loisirs + data.shopping + data.autres
    epargne = data.revenu - total
    taux = round(epargne / data.revenu * 100, 1) if data.revenu > 0 else 0

    categories = [
        {"nom": "Logement", "valeur": data.loyer + data.charges},
        {"nom": "Alimentation", "valeur": data.courses},
        {"nom": "Transport", "valeur": data.transport},
        {"nom": "Téléphone", "valeur": data.telephone},
        {"nom": "Santé", "valeur": data.sante},
        {"nom": "Loisirs", "valeur": data.loisirs},
        {"nom": "Shopping", "valeur": data.shopping},
        {"nom": "Autres", "valeur": data.autres}
    ]

    recommandations = []
    if (data.loyer / data.revenu * 100) > 33:
        recommandations.append({"type": "danger", "text": f"Votre loyer représente {(data.loyer/data.revenu*100):.0f}% de vos revenus"})
    if taux < 10:
        recommandations.append({"type": "warning", "text": f"Taux d'épargne de {taux}%. Objectif: 10% minimum"})
    if taux >= 20:
        recommandations.append({"type": "success", "text": f"Excellent ! Vous épargnez {taux}%"})

    return {
        "total_depenses": round(total, 2),
        "epargne": round(epargne, 2),
        "taux_epargne": taux,
        "categories": categories,
        "recommandations": recommandations,
        "objectif_urgence": round(data.revenu * 3, 2)
    }

# --- OPCVM Simulator ---
class OPCVMSimInput(BaseModel):
    montant_initial: float
    duree_annees: int
    versement_mensuel: float
    rendement_annuel: float = 6.5

@router.post("/opcvm-sim")
def calculate_opcvm_sim(data: OPCVMSimInput):
    taux_mensuel = data.rendement_annuel / 100 / 12
    nb_mois = data.duree_annees * 12

    valeur_finale = data.montant_initial * pow(1 + taux_mensuel, nb_mois) + data.versement_mensuel * (pow(1 + taux_mensuel, nb_mois) - 1) / taux_mensuel
    total_verse = data.montant_initial + data.versement_mensuel * nb_mois
    gains = valeur_finale - total_verse

    return {
        "total_verse": round(total_verse, 2),
        "valeur_finale": round(valeur_finale, 2),
        "gains": round(gains, 2),
        "performance_totale": round((gains / total_verse * 100), 1) if total_verse > 0 else 0
    }
