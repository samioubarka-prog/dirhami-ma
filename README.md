# 🇲🇦 Dirhami (درهمي) - Plateforme Financière Maroc

Plateforme web complète pour comparer et simuler les produits financiers au Maroc.

## 🚀 Fonctionnalités

- **💳 Comparateur Cartes Bancaires** - Comparez les frais, plafonds et avantages
- **📈 Comparateur OPCVM** - Fonds d'investissement avec rendements et frais
- **🏠 Simulateur Crédit Immobilier** - Mensualité et tableau d'amortissement
- **👴 Simulateur Retraite** - Pension CNSS/CMR/RCAR + épargne complémentaire
- **💰 Simulateur Budget** - Gestion budgétaire avec recommandations
- **📋 Fiscalité** - Régimes de retraite, PEA, Daam Iskane, impôts
- **📝 Blog** - 20 articles sur la finance au Maroc
- **🔐 Authentification JWT** - Inscription, connexion, sauvegarde des simulations

## 🏗️ Architecture

```
dirhami-ma-v2/
├── backend/           # FastAPI + SQLAlchemy + PostgreSQL
│   ├── app/
│   │   ├── routers/   # API endpoints (auth, cartes, opcvm, calculators...)
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── main.py    # Application entry point
│   │   ├── database.py
│   │   ├── security.py
│   │   └── config.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/          # Site statique HTML/CSS/JS
│   ├── index.html
│   ├── cartes-bancaires.html
│   ├── opcvm.html
│   ├── credit-immobilier.html
│   ├── retraite.html
│   ├── budget.html
│   ├── fiscalite.html
│   ├── js/
│   ├── css/
│   └── blog/
├── deploy/
└── render.yaml        # Configuration Render.com
```

## 🛠️ Technologies

**Backend:**
- FastAPI (Python 3.11)
- SQLAlchemy ORM
- PostgreSQL
- JWT Authentication
- Docker

**Frontend:**
- HTML5 / CSS3
- Bootstrap 5
- Vanilla JavaScript
- Chart.js

## 🚀 Déploiement sur Render

1. Fork/push ce repo sur GitHub
2. Connectez Render à votre repo
3. Render détectera automatiquement le `render.yaml`
4. Le service backend et la base de données PostgreSQL seront créés automatiquement
5. Le frontend statique sera déployé sur un domaine séparé

## 🧪 Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/
```

## 📊 Données

Les données des cartes bancaires et OPCVM sont basées sur les informations publiques des banques marocaines et de l'AMMC (Mai 2026).

## ⚠️ Avertissement

Les simulations et comparatifs sont fournis à titre indicatif. Consultez un conseiller financier agréé avant toute décision d'investissement ou de crédit.

## 📜 Licence

MIT License - Projet open source
