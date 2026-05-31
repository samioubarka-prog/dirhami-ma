# 🇲🇦 Dirhami - Plateforme Financière Maroc

**Dirhami** est une plateforme web gratuite qui permet aux Marocains de comparer et optimiser leurs finances personnelles.

## 🚀 Fonctionnalités

- 💳 **Comparateur de Cartes Bancaires** - Comparez les frais de +18 cartes
- 🏠 **Simulateur Crédit Immobilier** - Calculez vos mensualités et tableau d'amortissement
- 📊 **Comparateur OPCVM** - Analysez les rendements et frais de gestion
- 🐷 **Planificateur Retraite** - Planifiez votre future retraite
- 💰 **Simulateur Budget** - Gérez votre budget avec la règle 50/30/20
- 🛡️ **Régimes d'Épargne** - PER, PEA, Assurance-vie et fiscalité

## 🛠️ Technologies

- **Backend** : FastAPI (Python)
- **Frontend** : HTML5, CSS3, Vanilla JavaScript
- **Graphiques** : Chart.js
- **Hébergement** : Render (Gratuit)

## 📦 Déploiement

### Option 1 : Render (Gratuit)

1. Fork ce repo sur GitHub
2. Crée un compte sur [Render](https://render.com)
3. Clique "New Web Service"
4. Connecte ton repo GitHub
5. Render détectera automatiquement `render.yaml`
6. Clique "Deploy"

### Option 2 : Local

```bash
# Cloner le repo
git clone https://github.com/TON-USER/dirhami.git
cd dirhami

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
uvicorn main:app --reload
```

Accède à `http://localhost:8000`

## 📁 Structure du projet

```
dirhami/
├── main.py                 # Backend FastAPI
├── requirements.txt        # Dépendances Python
├── render.yaml            # Configuration Render
├── index.html             # Page d'accueil
├── cartes-bancaires.html  # Comparateur cartes
├── credit-immobilier.html # Simulateur crédit
├── opcvm.html             # Comparateur OPCVM
├── retraite.html          # Planificateur retraite
├── budget.html            # Simulateur budget
├── regimes-epargne.html   # Régimes épargne & impôts
├── contact.html           # Page contact
├── css/
│   └── style.css          # Styles principaux
├── js/
│   ├── main.js            # Scripts utils
│   ├── cartes-data.js     # Données cartes bancaires
│   └── opcvm-data.js      # Données OPCVM
└── images/                # Images et logos
```

## 📊 Données

Les données des banques et OPCVM sont basées sur les tarifs publics disponibles en 2026. Elles sont mises à jour régulièrement.

## ⚠️ Avertissement

Dirhami est une plateforme d'information. Les simulations sont indicatives. Consultez toujours un conseiller financier avant de prendre des décisions d'investissement.

## 📄 Licence

MIT License - Libre d'utilisation et de modification.

---

Made with ❤️ in Morocco 🇲🇦
