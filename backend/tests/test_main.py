from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_calculators_credit():
    payload = {
        "prix_bien": 800000,
        "apport": 160000,
        "taux_annuel": 4.35,
        "duree_annees": 20,
        "type_credit": "classique",
        "taux_assurance": 0.36,
        "frais_dossier_pct": 1.0
    }
    response = client.post("/api/v1/calculators/credit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["montant_emprunt"] == 640000
    assert data["mensualite_hors_assurance"] > 0

def test_calculators_retraite():
    payload = {
        "age_actuel": 35,
        "age_retraite": 60,
        "salaire": 15000,
        "regime": "cnss",
        "annees_cotisees": 10,
        "epargne_actuelle": 50000,
        "versement_mensuel": 1000,
        "rendement": 5
    }
    response = client.post("/api/v1/calculators/retraite", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["pension_base"] > 0

def test_calculators_budget():
    payload = {
        "revenu": 15000,
        "loyer": 4000,
        "charges": 800,
        "courses": 2500,
        "transport": 1000,
        "telephone": 300,
        "sante": 500,
        "loisirs": 800,
        "shopping": 600,
        "autres": 500
    }
    response = client.post("/api/v1/calculators/budget", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["epargne"] == 3000
