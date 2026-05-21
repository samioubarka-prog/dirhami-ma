# Dirhami - Plateforme Financière du Maroc

**Dirhami** (درهمي) est une plateforme web complète de comparaison et simulation financière pour le Maroc, inspirée de wafir.ma et tamra.ma.

## Fonctionnalités

### Comparateurs
- **Cartes Bancaires** : Comparez les frais, assurances et avantages de 12 cartes des principales banques marocaines
- **Crédits Immobiliers** : Simulez votre crédit habitat avec tableau d'amortissement complet
- **OPCVM** : Comparez les rendements, frais de gestion et performances des fonds d'investissement

### Simulateurs
- **Planification Retraite** : Vérifiez si vous êtes sur la bonne voie
- **Gestion Budget** : Analysez votre budget et optimisez votre épargne
- **Calculateur Fiscal** : Découvrez les économies d'impôt possibles

### Informations
- **Guide Fiscal** : PEA, déduction IR, assurance vie, PER
- **Blog** : Conseils et actualités financières

## Architecture Technique

### Backend (FastAPI)
- **Framework** : FastAPI (Python)
- **Base de données** : PostgreSQL + SQLAlchemy
- **Authentification** : JWT (JSON Web Tokens)
- **API REST** : Documentation automatique via Swagger/OpenAPI

### Frontend (Vanilla JS)
- **HTML/CSS/JS** pur (pas de framework lourd)
- **Graphiques** : Chart.js
- **Responsive** : Design mobile-first
- **Icônes** : Font Awesome

### Données
- 12 cartes bancaires (Attijariwafa, BMCE, CIH, Crédit du Maroc, Bank of Africa, BMCI)
- 10 offres de crédit immobilier avec TAEG réels
- 15 OPCVM avec rendements et frais réels
- 8 régimes fiscaux marocains

## Structure du Projet

```
dirhami-ma-v2/
├── backend/
│   ├── app/
│   │   ├── data/
│   │   │   ├── bank_cards.json
│   │   │   ├── mortgage_rates.json
│   │   │   ├── opcvm.json
│   │   │   └── tax_regimes.json
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── bank_cards.py
│   │   │   ├── mortgage.py
│   │   │   ├── opcvm.py
│   │   │   ├── simulations.py
│   │   │   └── tax_regimes.py
│   │   ├── services/
│   │   │   ├── auth.py
│   │   │   └── calculations.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── config.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   └── pages/
│   │       ├── cartes.js
│   │       ├── credit.js
│   │       ├── opcvm.js
│   │       ├── retraite.js
│   │       ├── budget.js
│   │       └── fiscalite.js
│   ├── pages/
│   │   ├── cartes.html
│   │   ├── credit.html
│   │   ├── opcvm.html
│   │   ├── retraite.html
│   │   ├── budget.html
│   │   ├── fiscalite.html
│   │   ├── blog.html
│   │   └── login.html
│   └── index.html
├── deploy/
│   └── (scripts de déploiement)
└── README.md
```

## Installation Locale

### 1. Prérequis
- Python 3.9+
- PostgreSQL 13+
- Node.js (optionnel, pour serveur frontend)

### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration Base de Données
```bash
# Créer la base de données PostgreSQL
createdb dirhami_db

# Modifier le fichier .env avec vos credentials
# DATABASE_URL=postgresql://user:password@localhost:5432/dirhami_db
```

### 4. Lancer le Backend
```bash
python -m app.main
# ou
uvicorn app.main:app --reload
```

L'API sera disponible sur http://localhost:8000
Documentation API : http://localhost:8000/api/docs

### 5. Frontend
Le frontend est en HTML/CSS/JS statique. Vous pouvez l'ouvrir directement dans le navigateur ou utiliser un serveur local :

```bash
cd frontend
# Avec Python
python -m http.server 5500

# Avec Node.js
npx serve -l 5500
```

Le frontend sera disponible sur http://localhost:5500

## Déploiement sur Hostinger

### Option 1 : VPS Hostinger

1. **Créer un VPS** (Ubuntu 22.04 recommandé)
2. **Se connecter en SSH** : `ssh root@votre-ip`
3. **Installer les dépendances** :
```bash
apt update && apt upgrade -y
apt install python3-pip python3-venv postgresql nginx -y
```

4. **Configurer PostgreSQL** :
```bash
sudo -u postgres psql -c "CREATE USER dirhami_user WITH PASSWORD 'votre_mot_de_passe';"
sudo -u postgres psql -c "CREATE DATABASE dirhami_db OWNER dirhami_user;"
```

5. **Déployer le projet** :
```bash
cd /var/www
git clone https://github.com/votre-compte/dirhami.git
cd dirhami/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Configurer Gunicorn** (créer `/etc/systemd/system/dirhami.service`) :
```ini
[Unit]
Description=Dirhami API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/dirhami/backend
Environment="PATH=/var/www/dirhami/backend/venv/bin"
ExecStart=/var/www/dirhami/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

7. **Configurer Nginx** (créer `/etc/nginx/sites-available/dirhami`) :
```nginx
server {
    listen 80;
    server_name dirhami.ma www.dirhami.ma;

    location / {
        root /var/www/dirhami/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

8. **Activer le site** :
```bash
ln -s /etc/nginx/sites-available/dirhami /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
systemctl enable dirhami
systemctl start dirhami
```

9. **SSL avec Certbot** :
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d dirhami.ma -d www.dirhami.ma
```

### Option 2 : Déploiement sur Render (Gratuit)

1. Créer un compte sur [Render](https://render.com)
2. Créer un nouveau Web Service
3. Connecter votre repo GitHub
4. Configurer :
   - **Build Command** : `pip install -r backend/requirements.txt`
   - **Start Command** : `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment** : Python 3
5. Ajouter les variables d'environnement (DATABASE_URL, SECRET_KEY)
6. Déployer !

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/auth/register` | Inscription |
| `POST /api/auth/login` | Connexion |
| `GET /api/auth/me` | Profil utilisateur |
| `GET /api/bank-cards/` | Liste des cartes |
| `GET /api/bank-cards/{id}` | Détail carte |
| `GET /api/bank-cards/compare/` | Comparaison cartes |
| `GET /api/mortgage/rates` | Taux crédits |
| `POST /api/mortgage/simulate` | Simulation crédit |
| `GET /api/opcvm/` | Liste OPCVM |
| `POST /api/opcvm/simulate` | Simulation OPCVM |
| `POST /api/simulations/retirement` | Simulation retraite |
| `POST /api/simulations/budget/analyze` | Analyse budget |
| `GET /api/tax-regimes/` | Régimes fiscaux |
| `GET /api/tax-regimes/calculator/deduction` | Calculateur déduction |

## Mise à jour des Données

Les données bancaires sont stockées en JSON. Pour mettre à jour :
1. Modifier les fichiers dans `backend/app/data/`
2. Redémarrer le serveur

Pour un scraping automatique, vous pouvez créer un script Python avec BeautifulSoup/Scrapy et l'exécuter régulièrement via cron.

## Auteur

**Dirhami** - Plateforme financière pour le Maroc

## Licence

Ce projet est sous licence MIT.

---

**Note** : Les données financières sont fournies à titre indicatif. Vérifiez toujours les informations directement auprès des banques et institutions concernées avant de prendre une décision financière.
