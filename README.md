# Dirhami (درهمي)

Plateforme financiere marocaine - Comparateur bancaire, simulateurs d'investissement et de credit.

## Fonctionnalites

- **Comparateur bancaire**: Comparez les banques conventionnelles et participatives du Maroc
- **Simulateur d'investissement**: Calculez vos rendements avec interets composes
- **Calculateur de credit immobilier**: Mensualites et tableau d'amortissement (amortissable & in fine)
- **Simulateur de retraite**: Projection du capital et pension mensuelle
- **Blog**: Guides financiers sur l'epargne, l'investissement, le credit et l'assurance au Maroc
- **Authentification**: Inscription/connexion avec JWT

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy + SQLite/PostgreSQL
- **Frontend**: HTML/CSS/JS Vanilla + Chart.js
- **Auth**: JWT + bcrypt
- **Deployment**: Render.com (Web Service + PostgreSQL)

## Installation locale

```bash
# 1. Cloner le repo
git clone https://github.com/votre-username/dirhami.git
cd dirhami

# 2. Creer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Installer les dependances
pip install -r requirements.txt

# 4. Lancer l'application
uvicorn app.main:app --reload

# 5. Ouvrir http://localhost:8000
```

## Deploiement sur Render

1. **Creer un compte** sur [render.com](https://render.com)
2. **New Web Service** -> Connecter votre repo GitHub
3. **Configuration**:
   - Build Command: `pip install -r requirements.txt && alembic upgrade head`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **New PostgreSQL**: Plan gratuit
5. **Environment Variables**:
   - `DATABASE_URL`: (auto-genere par Render)
   - `SECRET_KEY`: (genere automatiquement)

Le fichier `render.yaml` est inclus pour le deploiement Blueprint.

## API Endpoints

| Endpoint | Methode | Description |
|----------|---------|-------------|
| `/api/auth/register` | POST | Inscription |
| `/api/auth/login` | POST | Connexion |
| `/api/auth/me` | GET | Profil utilisateur |
| `/api/banks/` | GET | Liste des banques |
| `/api/blog/` | GET | Articles du blog |
| `/api/calculators/investment` | POST | Simulateur investissement |
| `/api/calculators/loan` | POST | Calculateur pret |
| `/api/calculators/retirement` | POST | Simulateur retraite |
| `/api/contacts/` | POST | Envoyer un message |

## Domaine suggere

**dirhami.ma** ou **dirhami.com**

"Dirhami" (درهمي) = synonyme d'epargne en darija marocaine.

## License

MIT
