# Dirhami.ma - Plateforme Financière Maroc

## Structure du projet

```
dirhami-ma/
├── backend/
│   ├── app.py              # Serveur Flask API
│   └── requirements.txt    # Dépendances Python
├── frontend/
│   ├── index.html
│   ├── comparateur-cartes.html
│   ├── comparateur-opcvm.html
│   ├── simulateur-credit.html
│   ├── simulateur-retraite.html
│   ├── simulateur-budget.html
│   ├── simulateur-investissement.html
│   ├── regimes-fiscaux.html
│   ├── blog.html
│   ├── article.html
│   └── css/style.css
└── render.yaml             # Configuration Render
```

## Déploiement sur Render

1. Connecter le repo GitHub à Render
2. Build Command: `pip install -r backend/requirements.txt`
3. Start Command: `gunicorn backend.app:app`
4. Le serveur démarre sur le port défini par la variable d'environnement PORT

## Fonctionnalités

- Comparateur cartes bancaires (20 cartes, filtres, détails)
- Comparateur OPCVM (12 fonds, détail comme tamra.ma)
- Simulateur crédit immobilier (tableau d'amortissement)
- Simulateur retraite (évolution du capital)
- Simulateur budget familial (répartition graphique)
- Simulateur investissement (intérêts composés)
- Régimes fiscaux (guide complet)
- Blog (20 articles)
