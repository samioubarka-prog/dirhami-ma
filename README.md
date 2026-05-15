# Dirhami.ma - Plateforme Financière Maroc

## 🎯 Présentation
**Dirhami.ma** est une plateforme web complète de comparaison et simulation financière pour le Maroc, inspirée de **tamra.ma** et **North Wallet**.

### Fonctionnalités
- ✅ **Comparateur de cartes bancaires** (20+ banques marocaines)
- ✅ **Comparateur OPCVM** (12 fonds d'investissement avec rendements et frais)
- ✅ **Simulateur crédit immobilier** (mensualité, tableau d'amortissement, taux d'endettement)
- ✅ **Simulateur retraite** (capital nécessaire, versements mensuels, projection graphique)
- ✅ **Simulateur investissement** (effet boule de neige, projection sur 30 ans)
- ✅ **Simulateur budget** (analyse des dépenses, suggestions d'économies)
- ✅ **Régimes fiscaux** (PEA, assurance-vie, déductions fiscales)
- ✅ **Blog** avec 6 articles financiers réels
- ✅ **Collecte d'emails** (popup style tamra.ma, formulaires, dashboard admin)
- ✅ **Dashboard Admin** avec statistiques et export CSV

---

## 🏗️ Architecture

```
dirhami-ma/
├── backend/
│   ├── app.py              # API Flask (Python) + SQLite
│   ├── requirements.txt    # Dépendances Python
│   └── database.db         # Base de données (créée auto)
│
├── frontend/
│   ├── index.html          # Page d'accueil
│   ├── comparateur-cartes.html
│   ├── comparateur-opcvm.html
│   ├── simulateur-credit.html
│   ├── simulateur-retraite.html
│   ├── simulateur-budget.html
│   ├── simulateur-investissement.html
│   ├── regimes-fiscaux.html
│   ├── blog.html
│   ├── article.html
│   ├── admin.html
│   ├── css/style.css       # Design premium responsive
│   └── js/main.js          # Logique frontend + API
│
├── deploy/
│   ├── dirhami.service     # Service systemd
│   ├── nginx.conf          # Config Nginx
│   └── install.sh          # Script d'installation
│
└── README.md
```

---

## 🚀 Déploiement étape par étape

### Étape 1 : Acheter le serveur VPS
Recommandé : **DigitalOcean, Hetzner, ou OVH Cloud**
- Ubuntu 22.04 LTS
- 2 vCPU, 2GB RAM minimum
- 25GB SSD
- Coût : ~5-10€/mois

### Étape 2 : Se connecter au serveur
```bash
ssh root@IP_DU_SERVEUR
```

### Étape 3 : Mettre à jour le système
```bash
apt update && apt upgrade -y
```

### Étape 4 : Installer Python et les dépendances
```bash
apt install -y python3 python3-pip python3-venv nginx git
```

### Étape 5 : Créer l'utilisateur et le dossier
```bash
useradd -m -s /bin/bash dirhami
mkdir -p /var/www/dirhami.ma
chown dirhami:dirhami /var/www/dirhami.ma
```

### Étape 6 : Copier les fichiers du projet
Sur votre ordinateur local, envoyez les fichiers :
```bash
scp -r dirhami-ma/* root@IP_DU_SERVEUR:/var/www/dirhami.ma/
```

### Étape 7 : Installer les dépendances Python
```bash
cd /var/www/dirhami.ma/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Étape 8 : Tester le backend
```bash
python app.py
```
Le serveur doit démarrer sur `http://localhost:5000`
Arrêtez avec `Ctrl+C`

### Étape 9 : Configurer Gunicorn
```bash
cp /var/www/dirhami.ma/deploy/dirhami.service /etc/systemd/system/
systemctl daemon-reload
systemctl start dirhami
systemctl enable dirhami
```

### Étape 10 : Configurer Nginx
```bash
cp /var/www/dirhami.ma/deploy/nginx.conf /etc/nginx/sites-available/dirhami.ma
ln -s /etc/nginx/sites-available/dirhami.ma /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Étape 11 : SSL avec Certbot
```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d dirhami.ma -d www.dirhami.ma
```

### Étape 12 : Configurer le domaine
Chez votre registrar :
- A Record : `@` → IP de votre serveur
- A Record : `www` → IP de votre serveur

---

## 📧 Collecte d'emails (style tamra.ma)
Le site collecte les emails via :
1. **Popup automatique** après 15s ou 50% de scroll
2. **Formulaire hero** sur la page d'accueil
3. **Section CTA** en bas de page
4. **Dashboard admin** accessible sur `/admin.html`

Tous les leads sont stockés dans `database.db` (SQLite) et exportables en CSV.

---

**© 2026 Dirhami.ma - Tous droits réservés**
