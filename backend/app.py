#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__, static_folder='../frontend')
CORS(app)
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL UNIQUE, nom TEXT, telephone TEXT, objet TEXT, date_inscription TEXT DEFAULT CURRENT_TIMESTAMP, source TEXT DEFAULT 'homepage')")
    cursor.execute("CREATE TABLE IF NOT EXISTS simulations (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT NOT NULL, params TEXT, resultats TEXT, email TEXT, date_creation TEXT DEFAULT CURRENT_TIMESTAMP)")
    cursor.execute("CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, titre TEXT NOT NULL, slug TEXT UNIQUE, categorie TEXT, contenu TEXT, image TEXT, date_pub TEXT DEFAULT CURRENT_TIMESTAMP, lu INTEGER DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS opcvm (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, categorie TEXT, societe TEXT, rendement_1an REAL, rendement_3ans REAL, frais_gestion REAL, frais_entree REAL, frais_sortie REAL, risque TEXT, min_investissement REAL, actif_total REAL, description TEXT, composition TEXT, performance_ytd REAL, volatilite REAL, last_update TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS cartes (id INTEGER PRIMARY KEY AUTOINCREMENT, banque TEXT, nom_carte TEXT, type TEXT, frais_annuels REAL, retrait_dab_national REAL, retrait_dab_international REAL, paiement_national REAL, paiement_international REAL, plafond_retrait_jour REAL, plafond_paiement_jour REAL, plafond_internet REAL, assurance_voyage INTEGER, cashback REAL, avantages TEXT, contactless INTEGER, detail_retrait_national TEXT, detail_retrait_international TEXT, detail_paiement_national TEXT, detail_paiement_international TEXT, detail_plafond TEXT, detail_assurance TEXT, detail_cashback TEXT, detail_contactless TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS credits (id INTEGER PRIMARY KEY AUTOINCREMENT, banque TEXT, taux_debiteur_min REAL, taux_debiteur_max REAL, taeg_min REAL, taeg_max REAL, frais_dossier TEXT, taux_assurance REAL, duree_max INTEGER, apport_min REAL, endettement_max REAL, conditions TEXT)")
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM opcvm")
    if cursor.fetchone()[0] == 0:
        opcvm_data = [("Attijari Valeurs","Actions","Attijari Intermediation",18.5,45.2,2.0,0.0,0.0,"Élevé",1000,850000000,"Fonds actions diversifié Bourse de Casablanca","Actions marocaines 85%, Liquidités 15%",22.3,18.5,"2026-05-15"),("BMCE Capital Croissance","Mixte","BMCE Capital",12.3,32.1,1.8,0.0,0.0,"Moyen",500,420000000,"Allocation équilibrée actions/obligations","Actions 50%, Obligations 40%, Liquidités 10%",14.2,12.1,"2026-05-15"),("CIH Actions","Actions","CIH Capital",15.2,38.7,2.2,0.0,0.0,"Élevé",1000,310000000,"Actions marocaines à forte croissance","Actions 90%, Liquidités 10%",18.1,19.2,"2026-05-15"),("Wafa Immobilier","Immobilier","Wafa Gestion",8.5,22.4,1.5,0.0,0.0,"Faible",500,280000000,"SCPI et OPCI immobiliers marocains","Immobilier 80%, Obligations 15%, Liquidités 5%",9.2,5.8,"2026-05-15"),("CDG Capital Prudent","Obligataire","CDG Capital",6.2,18.5,1.0,0.0,0.0,"Faible",500,950000000,"Obligations souveraines et corporate","Obligations 85%, Actions 10%, Liquidités 5%",6.8,3.2,"2026-05-15"),("Al Mada Monétaire","Monétaire","Al Mada Gestion",4.1,12.8,0.6,0.0,0.0,"Très faible",1000,1200000000,"Trésorerie et placements courts terme","Bons de trésor 70%, Dépôts 25%, Liquidités 5%",4.3,0.8,"2026-05-15"),("BCP Actions","Actions","BCP Capital",14.8,35.6,2.0,0.0,0.0,"Élevé",1000,275000000,"Actions grandes et moyennes capitalisations","Actions 88%, Liquidités 12%",16.5,17.8,"2026-05-15"),("Saham Obligations","Obligataire","Saham Gestion",7.1,20.3,1.2,0.0,0.0,"Faible",500,540000000,"Obligations à revenus réguliers","Obligations 90%, Liquidités 10%",7.5,3.5,"2026-05-15"),("CFG Dynamique","Mixte","CFG Gestion",11.5,28.4,1.6,0.0,0.0,"Moyen",500,180000000,"Allocation flexible selon marchés","Actions 45%, Obligations 45%, Liquidités 10%",13.1,10.2,"2026-05-15"),("Attijari Obligataire","Obligataire","Attijari Intermediation",6.8,19.2,1.1,0.0,0.0,"Faible",1000,620000000,"Obligations publiques et privées","Obligations 88%, Actions 7%, Liquidités 5%",7.2,3.1,"2026-05-15"),("BMCE Monétaire","Monétaire","BMCE Capital",3.8,11.5,0.5,0.0,0.0,"Très faible",500,890000000,"Placement liquidité court terme","Bons de trésor 75%, Dépôts 20%, Liquidités 5%",4.0,0.6,"2026-05-15"),("CDG Actions","Actions","CDG Capital",16.2,41.3,2.1,0.0,0.0,"Élevé",1000,340000000,"Actions à dividendes et croissance","Actions 87%, Liquidités 13%",19.4,18.9,"2026-05-15")]
        cursor.executemany("INSERT INTO opcvm (nom, categorie, societe, rendement_1an, rendement_3ans, frais_gestion, frais_entree, frais_sortie, risque, min_investissement, actif_total, description, composition, performance_ytd, volatilite, last_update) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", opcvm_data)
    cursor.execute("SELECT COUNT(*) FROM cartes")
    if cursor.fetchone()[0] == 0:
        cartes_data = [("Attijariwafa Bank","Carte Visa Classic","Visa Classic",150,8.0,15.0,0,0,5000,20000,10000,0,0.0,"E-banking, SMS alerts, 3D Secure",1,"Gratuit dans le réseau Attijariwafa","15 MAD + 2.5% hors réseau","Gratuit au Maroc","Gratuit au Maroc","5 000 MAD/jour retrait, 20 000 MAD/jour paiement","Non incluse","Aucun","Disponible"),("Attijariwafa Bank","Carte Visa Gold","Visa Gold",350,6.0,12.0,0,0,10000,50000,20000,1,0.0,"Assurance voyage, Concierge, Lounge access",1,"Gratuit dans le réseau Attijariwafa","12 MAD + 2% hors réseau","Gratuit au Maroc","Gratuit au Maroc","10 000 MAD/jour retrait, 50 000 MAD/jour paiement","Assurance voyage jusqu'à 100 000 €","Aucun","Disponible"),("Attijariwafa Bank","Carte Visa Platinum","Visa Platinum",700,4.0,10.0,0,0,20000,100000,50000,1,0.5,"Lounge access, Cashback 0.5%, Concierge premium",1,"Gratuit dans le réseau Attijariwafa","10 MAD + 1.5% hors réseau","Gratuit au Maroc","Gratuit au Maroc","20 000 MAD/jour retrait, 100 000 MAD/jour paiement","Assurance voyage jusqu'à 250 000 €","0.5% sur tous les achats","Disponible"),("BMCE Bank","Carte Visa Classic","Visa Classic",120,8.0,15.0,0,0,4000,15000,8000,0,0.0,"E-banking, Attijari Mobile",1,"Gratuit dans le réseau BMCE","15 MAD + 2.5% hors réseau","Gratuit au Maroc","Gratuit au Maroc","4 000 MAD/jour retrait, 15 000 MAD/jour paiement","Non incluse","Aucun","Disponible"),("BMCE Bank","Carte Visa Gold","Visa Gold",300,6.0,12.0,0,0,8000,40000,20000,1,0.0,"Assurance voyage, Assistance internationale",1,"Gratuit dans le réseau BMCE","12 MAD + 2% hors réseau","Gratuit au Maroc","Gratuit au Maroc","8 000 MAD/jour retrait, 40 000 MAD/jour paiement","Assurance voyage jusqu'à 100 000 €","Aucun","Disponible"),("BMCE Bank","Carte Visa Platinum","Visa Platinum",600,4.0,10.0,0,0,15000,80000,40000,1,1.0,"Lounge, Cashback 1%, Protection achats",1,"Gratuit dans le réseau BMCE","10 MAD + 1.5% hors réseau","Gratuit au Maroc","Gratuit au Maroc","15 000 MAD/jour retrait, 80 000 MAD/jour paiement","Assurance voyage jusqu'à 250 000 €","1% sur tous les achats","Disponible"),("CIH Bank","Carte Visa Classic","Visa Classic",100,8.0,15.0,0,0,3000,12000,6000,0,0.0,"E-banking, CIH Mobile",1,"Gratuit dans le réseau CIH","15 MAD + 2.5% hors réseau","Gratuit au Maroc","Gratuit au Maroc","3 000 MAD/jour retrait, 12 000 MAD/jour paiement","Non incluse","Aucun","Disponible"),("CIH Bank","Carte Visa Gold","Visa Gold",250,6.0,12.0,0,0,6000,30000,15000,1,0.0,"Assurance voyage, Assistance 24/7",1,"Gratuit dans le réseau CIH","12 MAD + 2% hors réseau","Gratuit au Maroc","Gratuit au Maroc","6 000 MAD/jour retrait, 30 000 MAD/jour paiement","Assurance voyage jusqu'à 100 000 €","Aucun","Disponible"),("CIH Bank","Carte Visa Platinum","Visa Platinum",500,4.0,10.0,0,0,12000,60000,30000,1,0.5,"Lounge access, Cashback 0.5%",1,"Gratuit dans le réseau CIH","10 MAD + 1.5% hors réseau","Gratuit au Maroc","Gratuit au Maroc","12 000 MAD/jour retrait, 60 000 MAD/jour paiement","Assurance voyage jusqu'à 250 000 €","0.5% sur tous les achats","Disponible"),("Crédit du Maroc","Carte Visa Classic","Visa Classic",130,8.0,15.0,0,0,3500,14000,7000,0,0.0,"E-banking, CDM Direct",1,"Gratuit dans le réseau CDM","15 MAD + 2.5% hors réseau","Gratuit au Maroc","Gratuit au Maroc","3 500 MAD/jour retrait, 14 000 MAD/jour paiement","Non incluse","Aucun","Disponible"),("Crédit du Maroc","Carte Visa Gold","Visa Gold",280,6.0,12.0,0,0,7000,35000,18000,1,0.0,"Assurance voyage, Concierge",1,"Gratuit dans le réseau CDM","12 MAD + 2% hors réseau","Gratuit au Maroc","Gratuit au Maroc","7 000 MAD/jour retrait, 35 000 MAD/jour paiement","Assurance voyage jusqu'à 100 000 €","Aucun","Disponible"),("BCP","Carte Visa Classic","Visa Classic",110,8.0,15.0,0,0,3500,13000,6500,0,0.0,"E-banking, BCP Mobile",1,"Gratuit dans le réseau BCP","15 MAD + 2.5% hors réseau","Gratuit au Maroc","Gratuit au Maroc","3 500 MAD/jour retrait, 13 000 MAD/jour paiement","Non incluse","Aucun","Disponible"),("BCP","Carte Visa Gold","Visa Gold",260,6.0,12.0,0,0,7000,32000,16000,1,0.0,"Assurance voyage, Assistance",1,"Gratuit dans le réseau BCP","12 MAD + 2% hors réseau","Gratuit au Maroc","Gratuit au Maroc","7 000 MAD/jour retrait, 32 000 MAD/jour paiement","Assurance voyage jusqu'à 100 000 €","Aucun","Disponible"),("CFG Bank","Carte Visa Classic","Visa Classic",90,8.0,15.0,0,0,3000,10000,5000,0,0.0,"E-banking, CFG Mobile",1,"Gratuit dans le réseau CFG","15 MAD + 2.5% hors réseau","Gratuit au Maroc","Gratuit au Maroc","3 000 MAD/jour retrait, 10 000 MAD/jour paiement","Non incluse","Aucun","Disponible"),("CFG Bank","Carte Visa Gold","Visa Gold",220,6.0,12.0,0,0,6000,25000,12000,1,0.0,"Assurance voyage, Assistance",1,"Gratuit dans le réseau CFG","12 MAD + 2% hors réseau","Gratuit au Maroc","Gratuit au Maroc","6 000 MAD/jour retrait, 25 000 MAD/jour paiement","Assurance voyage jusqu'à 100 000 €","Aucun","Disponible"),("CFG Bank","Carte Visa Platinum","Visa Platinum",450,4.0,10.0,0,0,10000,50000,25000,1,0.5,"Lounge, Cashback 0.5%, Concierge",1,"Gratuit dans le réseau CFG","10 MAD + 1.5% hors réseau","Gratuit au Maroc","Gratuit au Maroc","10 000 MAD/jour retrait, 50 000 MAD/jour paiement","Assurance voyage jusqu'à 250 000 €","0.5% sur tous les achats","Disponible"),("Société Générale Maroc","Carte Visa Classic","Visa Classic",140,8.0,15.0,0,0,4000,15000,7500,0,0.0,"E-banking, SG Mobile",1,"Gratuit dans le réseau SG","15 MAD + 2.5% hors réseau","Gratuit au Maroc","Gratuit au Maroc","4 000 MAD/jour retrait, 15 000 MAD/jour paiement","Non incluse","Aucun","Disponible"),("Société Générale Maroc","Carte Visa Gold","Visa Gold",320,6.0,12.0,0,0,8000,40000,20000,1,0.0,"Assurance voyage, Lounge",1,"Gratuit dans le réseau SG","12 MAD + 2% hors réseau","Gratuit au Maroc","Gratuit au Maroc","8 000 MAD/jour retrait, 40 000 MAD/jour paiement","Assurance voyage jusqu'à 100 000 €","Aucun","Disponible"),("Bank of Africa","Carte Visa Classic","Visa Classic",100,8.0,15.0,0,0,3000,12000,6000,0,0.0,"E-banking, BOA Mobile",1,"Gratuit dans le réseau BOA","15 MAD + 2.5% hors réseau","Gratuit au Maroc","Gratuit au Maroc","3 000 MAD/jour retrait, 12 000 MAD/jour paiement","Non incluse","Aucun","Disponible"),("Bank of Africa","Carte Visa Gold","Visa Gold",240,6.0,12.0,0,0,6000,30000,15000,1,0.0,"Assurance voyage, Assistance",1,"Gratuit dans le réseau BOA","12 MAD + 2% hors réseau","Gratuit au Maroc","Gratuit au Maroc","6 000 MAD/jour retrait, 30 000 MAD/jour paiement","Assurance voyage jusqu'à 100 000 €","Aucun","Disponible")]
        cursor.executemany("INSERT INTO cartes (banque, nom_carte, type, frais_annuels, retrait_dab_national, retrait_dab_international, paiement_national, paiement_international, plafond_retrait_jour, plafond_paiement_jour, plafond_internet, assurance_voyage, cashback, avantages, contactless, detail_retrait_national, detail_retrait_international, detail_paiement_national, detail_paiement_international, detail_plafond, detail_assurance, detail_cashback, detail_contactless) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", cartes_data)
    cursor.execute("SELECT COUNT(*) FROM credits")
    if cursor.fetchone()[0] == 0:
        credits_data = [("Attijariwafa Bank",5.8,7.2,6.5,8.1,"1% du capital",0.35,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),("BMCE Bank",5.9,7.5,6.6,8.3,"1% du capital",0.36,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),("CIH Bank",6.0,7.8,6.8,8.5,"0.5% - 1%",0.35,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),("Crédit du Maroc",6.2,8.0,7.0,8.8,"1% du capital",0.37,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),("BCP",6.0,7.6,6.7,8.4,"1% du capital",0.35,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),("CFG Bank",5.5,7.0,6.2,7.8,"0.5% - 1%",0.34,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),("Société Générale Maroc",5.7,7.3,6.4,8.0,"1% du capital",0.35,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),("Bank of Africa",5.8,7.4,6.5,8.1,"0.5% - 1%",0.35,25,10.0,40.0,"Revenus stables, CIN, fiche de paie")]
        cursor.executemany("INSERT INTO credits (banque, taux_debiteur_min, taux_debiteur_max, taeg_min, taeg_max, frais_dossier, taux_assurance, duree_max, apport_min, endettement_max, conditions) VALUES (?,?,?,?,?,?,?,?,?,?,?)", credits_data)
    cursor.execute("SELECT COUNT(*) FROM articles")
    if cursor.fetchone()[0] == 0:
        now = datetime.now().isoformat()
        articles_data = [("Guide complet du crédit immobilier au Maroc 2026","guide-credit-immobilier-2026","Immobilier","Contenu article 1...","credit.jpg",now,0),("PEA Maroc 2026 : Tout savoir sur le Plan d'Épargne en Actions","pea-maroc-guide-2026","Épargne","Contenu article 2...","pea.jpg",now,0),("OPCVM Maroc 2026 : Comment choisir son fonds ?","opcvm-choisir-fonds-2026","Investissement","Contenu article 3...","opcvm.jpg",now,0),("Régimes d'épargne retraite au Maroc 2026","regimes-retraite-maroc-2026","Retraite","Contenu article 4...","retraite.jpg",now,0),("Banques en ligne vs traditionnelles au Maroc 2026","banques-ligne-vs-traditionnelles-2026","Banques","Contenu article 5...","banques.jpg",now,0),("Investir en Bourse de Casablanca : Guide Débutant 2026","bourse-casablanca-debutant-2026","Investissement","Contenu article 6...","bourse.jpg",now,0),("Assurance-vie au Maroc : Guide complet 2026","assurance-vie-maroc-2026","Épargne","Contenu article 7...","assurance-vie.jpg",now,0),("Compte Épargne Logement (CEL) : Tout savoir 2026","compte-epargne-logement-2026","Immobilier","Contenu article 8...","cel.jpg",now,0),("Déductions fiscales épargne retraite au Maroc","deductions-fiscales-retraite-2026","Fiscalité","Contenu article 9...","fiscalite-retraite.jpg",now,0),("Cartes bancaires gratuites au Maroc : Mythe ou réalité ?","cartes-bancaires-gratuites-2026","Banques","Contenu article 10...","cartes-gratuites.jpg",now,0),("Immobilier locatif au Maroc : Rentabilité et fiscalité 2026","immobilier-locatif-maroc-2026","Immobilier","Contenu article 11...","immobilier-locatif.jpg",now,0),("Transfert d'argent international depuis le Maroc 2026","transfert-argent-international-2026","Banques","Contenu article 12...","transfert-international.jpg",now,0),("Cryptomonnaies au Maroc : Légalité et risques 2026","cryptomonnaies-maroc-2026","Investissement","Contenu article 13...","crypto.jpg",now,0),("Épargne salariale au Maroc : Intéressement et participation 2026","epargne-salariale-maroc-2026","Épargne","Contenu article 14...","epargne-salariale.jpg",now,0),("Crédit consommation vs crédit immobilier au Maroc","credit-conso-vs-immo-2026","Crédit","Contenu article 15...","credit-conso-vs-immo.jpg",now,0),("Fonds de sécurité : Combien épargner d'urgence au Maroc ?","fonds-securite-urgence-2026","Épargne","Contenu article 16...","fonds-securite.jpg",now,0),("Divorce et patrimoine au Maroc : Protéger ses biens","divorce-patrimoine-maroc-2026","Patrimoine","Contenu article 17...","divorce-patrimoine.jpg",now,0),("Héritage au Maroc : Transmission et optimisation fiscale 2026","heritage-maroc-2026","Patrimoine","Contenu article 18...","heritage.jpg",now,0),("Budget voyage au Maroc : Combien préparer ?","budget-voyage-maroc-2026","Budget","Contenu article 19...","budget-voyage.jpg",now,0),("Néo-banques au Maroc : La révolution digitale 2026","neo-banques-maroc-2026","Banques","Contenu article 20...","neo-banques.jpg",now,0)]
        cursor.executemany("INSERT INTO articles (titre, slug, categorie, contenu, image, date_pub, lu) VALUES (?,?,?,?,?,?,?)", articles_data)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

@app.route('/api/leads', methods=['POST'])
def create_lead():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO leads (email, nom, telephone, objet, source) VALUES (?, ?, ?, ?, ?)", (data.get('email'), data.get('nom'), data.get('telephone'), data.get('objet'), data.get('source', 'homepage')))
        conn.commit()
        return jsonify({"success": True, "message": "Inscription réussie !"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Cet email est déjà inscrit."}), 409
    finally:
        conn.close()

@app.route('/api/leads', methods=['GET'])
def get_leads():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY date_inscription DESC")
    leads = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(leads)

@app.route('/api/opcvm', methods=['GET'])
def get_opcvm():
    conn = get_db()
    cursor = conn.cursor()
    categorie = request.args.get('categorie')
    if categorie:
        cursor.execute("SELECT * FROM opcvm WHERE categorie = ?", (categorie,))
    else:
        cursor.execute("SELECT * FROM opcvm")
    opcvm = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(opcvm)

@app.route('/api/opcvm/<int:id>', methods=['GET'])
def get_opcvm_detail(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM opcvm WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "OPCVM non trouvé"}), 404

@app.route('/api/cartes', methods=['GET'])
def get_cartes():
    conn = get_db()
    cursor = conn.cursor()
    banque = request.args.get('banque')
    type_carte = request.args.get('type')
    query = "SELECT * FROM cartes WHERE 1=1"
    params = []
    if banque:
        query += " AND banque = ?"
        params.append(banque)
    if type_carte:
        query += " AND type = ?"
        params.append(type_carte)
    cursor.execute(query, params)
    cartes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(cartes)

@app.route('/api/cartes/banques', methods=['GET'])
def get_banques():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT banque FROM cartes")
    banques = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(banques)

@app.route('/api/credits', methods=['GET'])
def get_credits():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credits")
    credits = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(credits)

@app.route('/api/articles', methods=['GET'])
def get_articles():
    conn = get_db()
    cursor = conn.cursor()
    categorie = request.args.get('categorie')
    if categorie:
        cursor.execute("SELECT * FROM articles WHERE categorie = ? ORDER BY date_pub DESC", (categorie,))
    else:
        cursor.execute("SELECT * FROM articles ORDER BY date_pub DESC")
    articles = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(articles)

@app.route('/api/articles/<slug>', methods=['GET'])
def get_article(slug):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE slug = ?", (slug,))
    article = cursor.fetchone()
    if article:
        cursor.execute("UPDATE articles SET lu = lu + 1 WHERE slug = ?", (slug,))
        conn.commit()
        conn.close()
        return jsonify(dict(article))
    conn.close()
    return jsonify({"error": "Article non trouvé"}), 404

@app.route('/api/simulations', methods=['POST'])
def save_simulation():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO simulations (type, params, resultats, email) VALUES (?, ?, ?, ?)", (data.get('type'), json.dumps(data.get('params')), json.dumps(data.get('resultats')), data.get('email')))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM leads")
    total_leads = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM simulations")
    total_simulations = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM articles")
    total_articles = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM leads WHERE date(date_inscription) = date('now')")
    leads_today = cursor.fetchone()[0]
    conn.close()
    return jsonify({"total_leads": total_leads, "total_simulations": total_simulations, "total_articles": total_articles, "leads_today": leads_today})

@app.route('/api/simulateur/credit', methods=['POST'])
def simulate_credit():
    data = request.get_json()
    montant = float(data.get('montant', 0))
    apport = float(data.get('apport', 0))
    taux = float(data.get('taux', 6.5)) / 100
    duree = int(data.get('duree', 20))
    revenu = float(data.get('revenu', 15000))
    capital = montant - apport
    n = duree * 12
    taux_mensuel = taux / 12
    if taux_mensuel > 0:
        mensualite = capital * (taux_mensuel * (1 + taux_mensuel)**n) / ((1 + taux_mensuel)**n - 1)
    else:
        mensualite = capital / n
    cout_total = mensualite * n
    interets = cout_total - capital
    tableau = []
    solde = capital
    for i in range(1, min(n + 1, 13)):
        interet_mois = solde * taux_mensuel
        amortissement = mensualite - interet_mois
        solde -= amortissement
        tableau.append({"mois": i, "mensualite": round(mensualite, 2), "interet": round(interet_mois, 2), "amortissement": round(amortissement, 2), "solde": round(max(solde, 0), 2)})
    return jsonify({"mensualite": round(mensualite, 2), "cout_total": round(cout_total, 2), "interets": round(interets, 2), "capital": round(capital, 2), "tableau": tableau, "taux_endettement": round((mensualite / revenu) * 100, 2)})

@app.route('/api/simulateur/retraite', methods=['POST'])
def simulate_retraite():
    data = request.get_json()
    age_actuel = int(data.get('age_actuel', 30))
    age_retraite = int(data.get('age_retraite', 60))
    revenu_actuel = float(data.get('revenu_actuel', 10000))
    taux_remplacement = float(data.get('taux_remplacement', 70)) / 100
    rendement = float(data.get('rendement', 6)) / 100
    capital_existant = float(data.get('capital_existant', 0))
    annees = age_retraite - age_actuel
    besoin_mensuel = revenu_actuel * taux_remplacement
    besoin_annuel = besoin_mensuel * 12
    capital_necessaire = besoin_annuel / rendement if rendement > 0 else 0
    capital_a_constituer = max(capital_necessaire - capital_existant, 0)
    n = annees * 12
    taux_mensuel = rendement / 12
    if taux_mensuel > 0 and n > 0:
        versement_mensuel = capital_a_constituer * taux_mensuel / ((1 + taux_mensuel)**n - 1)
    else:
        versement_mensuel = capital_a_constituer / n if n > 0 else 0
    capital_projete = capital_existant
    evolution = []
    for a in range(annees + 1):
        if a > 0:
            capital_projete = (capital_projete + versement_mensuel * 12) * (1 + rendement)
        evolution.append({"annee": age_actuel + a, "capital": round(capital_projete, 2)})
    return jsonify({"capital_necessaire": round(capital_necessaire, 2), "versement_mensuel": round(versement_mensuel, 2), "besoin_mensuel": round(besoin_mensuel, 2), "annees_epargne": annees, "capital_projete": round(capital_projete, 2), "taux_remplacement": taux_remplacement * 100, "evolution": evolution})

@app.route('/api/simulateur/investissement', methods=['POST'])
def simulate_investissement():
    data = request.get_json()
    capital_initial = float(data.get('capital_initial', 0))
    versement_mensuel = float(data.get('versement_mensuel', 1000))
    rendement_annuel = float(data.get('rendement', 7)) / 100
    duree = int(data.get('duree', 10))
    taux_mensuel = rendement_annuel / 12
    n = duree * 12
    vf_capital = capital_initial * (1 + rendement_annuel)**duree
    vf_versements = versement_mensuel * ((1 + taux_mensuel)**n - 1) / taux_mensuel if taux_mensuel > 0 else versement_mensuel * n
    total = vf_capital + vf_versements
    capital_investi = capital_initial + (versement_mensuel * n)
    interets = total - capital_investi
    evolution = []
    capital = capital_initial
    for annee in range(duree + 1):
        if annee > 0:
            capital = capital * (1 + rendement_annuel) + versement_mensuel * 12
        evolution.append({"annee": annee, "capital": round(capital, 2)})
    return jsonify({"total": round(total, 2), "interets": round(interets, 2), "capital_investi": round(capital_investi, 2), "evolution": evolution, "performance": round((interets / capital_investi) * 100, 2) if capital_investi > 0 else 0})

@app.route('/api/simulateur/budget', methods=['POST'])
def simulate_budget():
    data = request.get_json()
    revenus = float(data.get('revenus', 0))
    loyer = float(data.get('loyer', 0))
    transport = float(data.get('transport', 0))
    nourriture = float(data.get('nourriture', 0))
    sante = float(data.get('sante', 0))
    loisirs = float(data.get('loisirs', 0))
    autres = float(data.get('autres', 0))
    objectif_epargne = float(data.get('objectif_epargne', 20))
    total_depenses = loyer + transport + nourriture + sante + loisirs + autres
    solde = revenus - total_depenses
    epargne_recommandee = revenus * (objectif_epargne / 100)
    suggestions = []
    if loyer > revenus * 0.33:
        suggestions.append("Votre loyer dépasse 33% de vos revenus. Envisagez un logement moins cher ou un colocataire.")
    if transport > revenus * 0.15:
        suggestions.append("Vos frais de transport sont élevés. Le covoiturage ou les transports en commun peuvent réduire cette dépense.")
    if loisirs > revenus * 0.1:
        suggestions.append("Vos dépenses de loisirs dépassent 10%. Réduisez les sorties ou choisissez des activités gratuites.")
    if nourriture > revenus * 0.2:
        suggestions.append("Votre budget nourriture est élevé. Faites vos courses en gros et cuisinez chez vous.")
    if solde < 0:
        suggestions.append("Vous êtes en déficit ! Réduisez immédiatement vos dépenses.")
    elif solde < epargne_recommandee:
        suggestions.append(f"Il vous manque {round(epargne_recommandee - solde, 0)} MAD/mois pour atteindre votre objectif d'épargne de {objectif_epargne}%.")
    else:
        suggestions.append(f"Bravo ! Vous pouvez épargner {round(solde, 0)} MAD/mois, ce qui dépasse votre objectif.")
    return jsonify({"total_depenses": round(total_depenses, 2), "solde": round(solde, 2), "epargne_recommandee": round(epargne_recommandee, 2), "taux_epargne": round((solde / revenus) * 100, 2) if revenus > 0 else 0, "taux_endettement": round((total_depenses / revenus) * 100, 2) if revenus > 0 else 0, "suggestions": suggestions, "repartition": {"loyer": loyer, "transport": transport, "nourriture": nourriture, "sante": sante, "loisirs": loisirs, "autres": autres, "epargne": max(solde, 0)}})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    print("=" * 50)
    print(" Dirhami.ma - Serveur démarré")
    print(" Base de données initialisée avec données 2026")
    print(f" Port: {port}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=False)
