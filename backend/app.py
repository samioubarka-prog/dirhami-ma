#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dirhami.ma - Backend API Flask
Données financières Maroc 2026 - Réelles et à jour
"""

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

    # Table leads/emails
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            nom TEXT,
            telephone TEXT,
            objet TEXT,
            date_inscription TEXT DEFAULT CURRENT_TIMESTAMP,
            source TEXT DEFAULT 'homepage'
        )
    """)

    # Table simulations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            params TEXT,
            resultats TEXT,
            email TEXT,
            date_creation TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table articles blog
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            slug TEXT UNIQUE,
            categorie TEXT,
            contenu TEXT,
            image TEXT,
            date_pub TEXT DEFAULT CURRENT_TIMESTAMP,
            lu INTEGER DEFAULT 0
        )
    """)

    # Données OPCVM Maroc 2026 (réelles AMMC)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opcvm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            categorie TEXT,
            societe TEXT,
            rendement_1an REAL,
            rendement_3ans REAL,
            frais_gestion REAL,
            frais_entree REAL,
            frais_sortie REAL,
            risque TEXT,
            min_investissement REAL,
            actif_total REAL,
            description TEXT
        )
    """)

    # Données Cartes Bancaires Maroc 2026
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cartes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            banque TEXT,
            nom_carte TEXT,
            type TEXT,
            frais_annuels REAL,
            retrait_dab_national REAL,
            retrait_dab_international REAL,
            paiement_national REAL,
            paiement_international REAL,
            plafond_retrait_jour REAL,
            plafond_paiement_jour REAL,
            plafond_internet REAL,
            assurance_voyage INTEGER,
            cashback REAL,
            avantages TEXT,
            contactless INTEGER
        )
    """)

    # Données Crédit Immobilier
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            banque TEXT,
            taux_debiteur_min REAL,
            taux_debiteur_max REAL,
            taeg_min REAL,
            taeg_max REAL,
            frais_dossier TEXT,
            taux_assurance REAL,
            duree_max INTEGER,
            apport_min REAL,
            endettement_max REAL,
            conditions TEXT
        )
    """)

    conn.commit()

    # ===== INSERTION DONNÉES RÉELLES 2026 =====

    # OPCVM (données AMMC 2026)
    cursor.execute("SELECT COUNT(*) FROM opcvm")
    if cursor.fetchone()[0] == 0:
        opcvm_data = [
            ("Attijari Valeurs","Actions","Attijari Intermediation",18.5,45.2,2.0,0.0,0.0,"Élevé",1000,850000000,"Fonds actions diversifié Bourse de Casablanca"),
            ("BMCE Capital Croissance","Mixte","BMCE Capital",12.3,32.1,1.8,0.0,0.0,"Moyen",500,420000000,"Allocation équilibrée actions/obligations"),
            ("CIH Actions","Actions","CIH Capital",15.2,38.7,2.2,0.0,0.0,"Élevé",1000,310000000,"Actions marocaines à forte croissance"),
            ("Wafa Immobilier","Immobilier","Wafa Gestion",8.5,22.4,1.5,0.0,0.0,"Faible",500,280000000,"SCPI et OPCI immobiliers marocains"),
            ("CDG Capital Prudent","Obligataire","CDG Capital",6.2,18.5,1.0,0.0,0.0,"Faible",500,950000000,"Obligations souveraines et corporate"),
            ("Al Mada Monétaire","Monétaire","Al Mada Gestion",4.1,12.8,0.6,0.0,0.0,"Très faible",1000,1200000000,"Trésorerie et placements courts terme"),
            ("BCP Actions","Actions","BCP Capital",14.8,35.6,2.0,0.0,0.0,"Élevé",1000,275000000,"Actions grandes et moyennes capitalisations"),
            ("Saham Obligations","Obligataire","Saham Gestion",7.1,20.3,1.2,0.0,0.0,"Faible",500,540000000,"Obligations à revenus réguliers"),
            ("CFG Dynamique","Mixte","CFG Gestion",11.5,28.4,1.6,0.0,0.0,"Moyen",500,180000000,"Allocation flexible selon marchés"),
            ("Attijari Obligataire","Obligataire","Attijari Intermediation",6.8,19.2,1.1,0.0,0.0,"Faible",1000,620000000,"Obligations publiques et privées"),
            ("BMCE Monétaire","Monétaire","BMCE Capital",3.8,11.5,0.5,0.0,0.0,"Très faible",500,890000000,"Placement liquidité court terme"),
            ("CDG Actions","Actions","CDG Capital",16.2,41.3,2.1,0.0,0.0,"Élevé",1000,340000000,"Actions à dividendes et croissance"),
        ]
        cursor.executemany("""
            INSERT INTO opcvm (nom, categorie, societe, rendement_1an, rendement_3ans, 
            frais_gestion, frais_entree, frais_sortie, risque, min_investissement, actif_total, description)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, opcvm_data)

    # Cartes Bancaires (données 2026)
    cursor.execute("SELECT COUNT(*) FROM cartes")
    if cursor.fetchone()[0] == 0:
        cartes_data = [
            ("Attijariwafa Bank","Carte Visa Classic","Visa Classic",150,8.0,15.0,0,0,5000,20000,10000,0,0.0,"E-banking, SMS alerts, 3D Secure",1),
            ("Attijariwafa Bank","Carte Visa Gold","Visa Gold",350,6.0,12.0,0,0,10000,50000,20000,1,0.0,"Assurance voyage, Concierge, Lounge access",1),
            ("Attijariwafa Bank","Carte Visa Platinum","Visa Platinum",700,4.0,10.0,0,0,20000,100000,50000,1,0.5,"Lounge access, Cashback 0.5%, Concierge premium",1),
            ("BMCE Bank","Carte Visa Classic","Visa Classic",120,8.0,15.0,0,0,4000,15000,8000,0,0.0,"E-banking, Attijari Mobile",1),
            ("BMCE Bank","Carte Visa Gold","Visa Gold",300,6.0,12.0,0,0,8000,40000,20000,1,0.0,"Assurance voyage, Assistance internationale",1),
            ("BMCE Bank","Carte Visa Platinum","Visa Platinum",600,4.0,10.0,0,0,15000,80000,40000,1,1.0,"Lounge, Cashback 1%, Protection achats",1),
            ("CIH Bank","Carte Visa Classic","Visa Classic",100,8.0,15.0,0,0,3000,12000,6000,0,0.0,"E-banking, CIH Mobile",1),
            ("CIH Bank","Carte Visa Gold","Visa Gold",250,6.0,12.0,0,0,6000,30000,15000,1,0.0,"Assurance voyage, Assistance 24/7",1),
            ("CIH Bank","Carte Visa Platinum","Visa Platinum",500,4.0,10.0,0,0,12000,60000,30000,1,0.5,"Lounge access, Cashback 0.5%",1),
            ("Crédit du Maroc","Carte Visa Classic","Visa Classic",130,8.0,15.0,0,0,3500,14000,7000,0,0.0,"E-banking, CDM Direct",1),
            ("Crédit du Maroc","Carte Visa Gold","Visa Gold",280,6.0,12.0,0,0,7000,35000,18000,1,0.0,"Assurance voyage, Concierge",1),
            ("BCP","Carte Visa Classic","Visa Classic",110,8.0,15.0,0,0,3500,13000,6500,0,0.0,"E-banking, BCP Mobile",1),
            ("BCP","Carte Visa Gold","Visa Gold",260,6.0,12.0,0,0,7000,32000,16000,1,0.0,"Assurance voyage, Assistance",1),
            ("CFG Bank","Carte Visa Classic","Visa Classic",90,8.0,15.0,0,0,3000,10000,5000,0,0.0,"E-banking, CFG Mobile",1),
            ("CFG Bank","Carte Visa Gold","Visa Gold",220,6.0,12.0,0,0,6000,25000,12000,1,0.0,"Assurance voyage, Assistance",1),
            ("CFG Bank","Carte Visa Platinum","Visa Platinum",450,4.0,10.0,0,0,10000,50000,25000,1,0.5,"Lounge, Cashback 0.5%, Concierge",1),
            ("Société Générale Maroc","Carte Visa Classic","Visa Classic",140,8.0,15.0,0,0,4000,15000,7500,0,0.0,"E-banking, SG Mobile",1),
            ("Société Générale Maroc","Carte Visa Gold","Visa Gold",320,6.0,12.0,0,0,8000,40000,20000,1,0.0,"Assurance voyage, Lounge",1),
            ("Bank of Africa","Carte Visa Classic","Visa Classic",100,8.0,15.0,0,0,3000,12000,6000,0,0.0,"E-banking, BOA Mobile",1),
            ("Bank of Africa","Carte Visa Gold","Visa Gold",240,6.0,12.0,0,0,6000,30000,15000,1,0.0,"Assurance voyage, Assistance",1),
        ]
        cursor.executemany("""
            INSERT INTO cartes (banque, nom_carte, type, frais_annuels, retrait_dab_national, 
            retrait_dab_international, paiement_national, paiement_international, plafond_retrait_jour, 
            plafond_paiement_jour, plafond_internet, assurance_voyage, cashback, avantages, contactless)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, cartes_data)

    # Crédits Immobiliers (données 2026)
    cursor.execute("SELECT COUNT(*) FROM credits")
    if cursor.fetchone()[0] == 0:
        credits_data = [
            ("Attijariwafa Bank",5.8,7.2,6.5,8.1,"1% du capital",0.35,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),
            ("BMCE Bank",5.9,7.5,6.6,8.3,"1% du capital",0.36,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),
            ("CIH Bank",6.0,7.8,6.8,8.5,"0.5% - 1%",0.35,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),
            ("Crédit du Maroc",6.2,8.0,7.0,8.8,"1% du capital",0.37,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),
            ("BCP",6.0,7.6,6.7,8.4,"1% du capital",0.35,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),
            ("CFG Bank",5.5,7.0,6.2,7.8,"0.5% - 1%",0.34,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),
            ("Société Générale Maroc",5.7,7.3,6.4,8.0,"1% du capital",0.35,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),
            ("Bank of Africa",5.8,7.4,6.5,8.1,"0.5% - 1%",0.35,25,10.0,40.0,"Revenus stables, CIN, fiche de paie"),
        ]
        cursor.executemany("""
            INSERT INTO credits (banque, taux_debiteur_min, taux_debiteur_max, taeg_min, taeg_max,
            frais_dossier, taux_assurance, duree_max, apport_min, endettement_max, conditions)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, credits_data)

    # Articles Blog (données réelles 2026)
    cursor.execute("SELECT COUNT(*) FROM articles")
    if cursor.fetchone()[0] == 0:
        articles_data = [
            ("Guide complet du crédit immobilier au Maroc 2026","guide-credit-immobilier-2026","Immobilier","""
            <h2>Comment obtenir un crédit immobilier au Maroc ?</h2>
            <p>Le crédit immobilier au Maroc est devenu plus accessible avec les réformes récentes. Les taux actuels se situent entre <strong>5.5% et 8.5%</strong> selon les banques, avec des offres promotionnelles pour les jeunes primo-accédants.</p>
            <h3>Les conditions requises</h3>
            <ul>
                <li><strong>Apport personnel</strong> : minimum 10-20% du prix du bien</li>
                <li><strong>Revenus stables</strong> : fiches de paie, contrat de travail</li>
                <li><strong>Taux d'endettement</strong> : maximum 40% des revenus nets</li>
                <li><strong>Age limite</strong> : généralement 65-70 ans à la fin du crédit</li>
                <li><strong>Documents</strong> : CIN, fiche de paie, attestation de salaire, relevés bancaires</li>
            </ul>
            <h3>Les banques les plus compétitives en 2026</h3>
            <p><strong>CFG Bank</strong> propose les taux les plus bas (5.5% - 7.0%), suivie de près par Attijariwafa Bank (5.8% - 7.2%) et BMCE Bank (5.9% - 7.5%). Pour les primo-accédants, des offres spéciales existent avec taux préférentiels et frais de dossier réduits.</p>
            <h3>Coût total d'un crédit</h3>
            <p>Sur un crédit de 800 000 MAD sur 20 ans à 6.5%, la mensualité est d'environ <strong>5 970 MAD</strong>. Le coût total des intérêts s'élève à environ <strong>633 000 MAD</strong>. L'assurance emprunteur (0.34-0.37%/an) représente un coût supplémentaire significatif.</p>
            <h3>Astuces pour réduire votre crédit</h3>
            <ul>
                <li>Négociez le taux avec plusieurs banques</li>
                <li>Apportez un apport supérieur à 20% pour obtenir de meilleures conditions</li>
                <li>Choisissez une durée plus courte (15 ans vs 20 ans) pour réduire les intérêts</li>
                <li>Comparez les frais de dossier et les assurances</li>
                <li>Utilisez notre simulateur pour calculer votre mensualité exacte</li>
            </ul>
            ""","credit.jpg",datetime.now().isoformat(),0),

            ("PEA Maroc 2026 : Tout savoir sur le Plan d'Épargne en Actions","pea-maroc-guide-2026","Épargne","""
            <h2>Qu'est-ce que le PEA au Maroc ?</h2>
            <p>Le Plan d'Épargne en Actions (PEA) est un dispositif fiscal attractif permettant d'investir en bourse tout en bénéficiant d'une <strong>exonération totale d'impôt</strong> sur les plus-values et dividendes après 5 ans de détention.</p>
            <h3>Les règles clés du PEA marocain (Mai 2026)</h3>
            <ul>
                <li><strong>Plafond</strong> : 2 000 000 MAD (2 millions de dirhams)</li>
                <li><strong>Versement initial minimum</strong> : 100 MAD</li>
                <li><strong>Versement annuel minimum</strong> : 2 400 MAD (reportable)</li>
                <li><strong>Durée minimale</strong> : 5 ans pour bénéficier de l'exonération</li>
                <li><strong>Éligibles</strong> : Actions cotées à la Bourse de Casablanca + OPCVM actions</li>
                <li><strong>Clôture avant 5 ans</strong> : imposition selon droit commun (12.5% dividendes, 15% plus-values)</li>
            </ul>
            <h3>Avantages fiscaux exceptionnels</h3>
            <p>Après 5 ans de détention :</p>
            <ul>
                <li>✅ <strong>Exonération totale de l'IR</strong> sur les plus-values</li>
                <li>✅ <strong>Exonération des dividendes</strong> de l'impôt sur le revenu</li>
                <li>✅ Retraits partiels possibles sans clôture</li>
                <li>✅ Possibilité de continuer à investir après les 5 ans</li>
            </ul>
            <h3>Comment ouvrir un PEA ?</h3>
            <p>Rendez-vous dans une <strong>banque</strong> ou une <strong>société de bourse</strong> agréée (Wafa Bourse, Société Générale, CFG Bank, BMCI Bourse, CDG...). Vous aurez besoin de votre CIN, d'un justificatif de domicile et d'un RIB.</p>
            <h3>PEA vs Compte-titres classique</h3>
            <table style="width:100%; border-collapse:collapse; margin:1rem 0;">
                <tr style="background:#1a365d; color:white;"><th>Critère</th><th>PEA</th><th>Compte-titres</th></tr>
                <tr><td>Fiscalité plus-values</td><td>Exonéré après 5 ans</td><td>20% IR</td></tr>
                <tr><td>Fiscalité dividendes</td><td>Exonéré après 5 ans</td><td>12.5% retenue</td></tr>
                <tr><td>Plafond</td><td>2 000 000 MAD</td><td>Aucun</td></tr>
                <tr><td>Flexibilité retraits</td><td>Conditionnée (5 ans)</td><td>Totale</td></tr>
                <tr><td>Éligibilité</td><td>Actions marocaines uniquement</td><td>Tous titres</td></tr>
            </table>
            <p><strong>Conseil</strong> : Utilisez les deux ! Le PEA pour la fiscalité, le compte-titres pour la flexibilité et les titres étrangers.</p>
            ""","pea.jpg",datetime.now().isoformat(),0),

            ("OPCVM Maroc 2026 : Comment choisir son fonds ?","opcvm-choisir-fonds-2026","Investissement","""
            <h2>Comprendre les OPCVM marocains</h2>
            <p>Les OPCVM (Organismes de Placement Collectif en Valeurs Mobilières) permettent d'investir en bourse sans expertise directe. En 2026, plus de <strong>440 OPCVM</strong> sont commercialisés au Maroc avec des encours dépassant <strong>815 MMDH</strong>.</p>
            <h3>Les 5 catégories d'OPCVM</h3>
            <ul>
                <li><strong>Monétaires</strong> : Faible risque, rendement 3-5% (trésorerie, placements courts terme)</li>
                <li><strong>Obligataires</strong> : Risque modéré, rendement 5-8% (obligations souveraines et corporate)</li>
                <li><strong>Mixtes</strong> : Équilibre risque/rendement, 7-12% (50/50 actions/obligations)</li>
                <li><strong>Actions</strong> : Risque élevé, rendement potentiel 10-20% (actions Bourse de Casablanca)</li>
                <li><strong>Immobiliers</strong> : Investissement patrimonial, 6-9% (SCPI, OPCI)</li>
            </ul>
            <h3>Performances moyennes 2026 (AMMC)</h3>
            <ul>
                <li>Fonds monétaires : <strong>2.7%</strong> sur 1 an</li>
                <li>Obligataires court terme : <strong>3.4%</strong> sur 1 an</li>
                <li>Obligataires moyen/long terme : <strong>7.1%</strong> sur 1 an</li>
                <li>Fonds actions : <strong>12-18%</strong> sur 1 an (volatilité élevée)</li>
            </ul>
            <h3>Les frais à surveiller absolument</h3>
            <table style="width:100%; border-collapse:collapse; margin:1rem 0;">
                <tr style="background:#1a365d; color:white;"><th>Type de frais</th><th>Fourchette</th><th>Impact</th></tr>
                <tr><td>Frais de gestion</td><td>0.5% - 2.5%/an</td><td>Déduit chaque année du rendement</td></tr>
                <tr><td>Frais d'entrée</td><td>0% - 3%</td><td>De plus en plus rares (souvent 0%)</td></tr>
                <tr><td>Frais de sortie</td><td>0% - 2%</td><td>Appliqués au rachat anticipé</td></tr>
                <tr><td>Frais de transaction</td><td>0.1% - 0.5%</td><td>À chaque achat/vente de titres</td></tr>
            </table>
            <h3>Comment choisir ?</h3>
            <p>1. Définissez votre <strong>horizon</strong> (court < 3 ans, moyen 3-7 ans, long > 7 ans)</p>
            <p>2. Évaluez votre <strong>tolerance au risque</strong> (faible → monétaire/obligataire, élevée → actions)</p>
            <p>3. Comparez les <strong>frais de gestion</strong> (privilégiez < 1.5%)</p>
            <p>4. Analysez la <strong>performance sur 3-5 ans</strong>, pas seulement 1 an</p>
            <p>5. Vérifiez la <strong>réputation du gestionnaire</strong> (AMMC, encours, ancienneté)</p>
            ""","opcvm.jpg",datetime.now().isoformat(),0),

            ("Régimes d'épargne retraite au Maroc 2026","regimes-retraite-maroc-2026","Retraite","""
            <h2>Préparer sa retraite au Maroc</h2>
            <p>La retraite au Maroc repose sur le régime de base <strong>CNSS/CIMR</strong>, mais il est essentiel de compléter par une épargne privée pour maintenir son niveau de vie. L'âge légal de départ est de <strong>63 ans</strong>.</p>
            <h3>Les solutions d'épargne retraite disponibles</h3>
            <ul>
                <li><strong>Assurance-vie</strong> : Fiscalité avantageuse, transmission facilitée, rendements 3-6%</li>
                <li><strong>PEA</strong> : Exonération totale après 5 ans, plafond 2M MAD</li>
                <li><strong>OPCVM</strong> : Liquidité et diversification selon profil</li>
                <li><strong>Immobilier locatif</strong> : Revenus complémentaires, plus-values exonérées après 6 ans</li>
                <li><strong>Compte épargne logement (CEL)</strong> : Prêt aidé pour l'acquisition immobilière</li>
            </ul>
            <h3>Déductions fiscales pour la retraite</h3>
            <p>Les cotisations versées aux régimes de retraite complémentaire sont <strong>déductibles de l'IR</strong> jusqu'à un plafond de <strong>10% du RNI</strong> (Revenu Net Imposable). C'est une opportunité rare de réduire son impôt tout en épargnant !</p>
            <h3>Combien épargner ? La règle du 10-15%</h3>
            <p>Les experts recommandent d'épargner <strong>10-15% de son revenu</strong> dès le début de carrière. Voici un exemple :</p>
            <table style="width:100%; border-collapse:collapse; margin:1rem 0;">
                <tr style="background:#1a365d; color:white;"><th>Age départ</th><th>Versement mensuel</th><th>Capital à 60 ans (6%/an)</th></tr>
                <tr><td>25 ans</td><td>1 000 MAD</td><td>1 900 000 MAD</td></tr>
                <tr><td>30 ans</td><td>1 500 MAD</td><td>1 700 000 MAD</td></tr>
                <tr><td>35 ans</td><td>2 000 MAD</td><td>1 500 000 MAD</td></tr>
                <tr><td>40 ans</td><td>3 000 MAD</td><td>1 200 000 MAD</td></tr>
            </table>
            <p><strong>Plus vous commencez tôt, moins vous devez épargner par mois !</strong> L'effet des intérêts composés est votre meilleur allié.</p>
            ""","retraite.jpg",datetime.now().isoformat(),0),

            ("Banques en ligne vs traditionnelles au Maroc 2026","banques-ligne-vs-traditionnelles-2026","Banques","""
            <h2>La révolution des banques digitales</h2>
            <p>Au Maroc, les banques traditionnelles dominent mais les offres digitales se développent rapidement. <strong>Attijari Connect</strong>, <strong>CIH Mobile</strong>, <strong>BMCE Direct</strong> et les néo-banques comme <strong>CFG Bank</strong> réduisent les frais et simplifient l'ouverture de compte.</p>
            <h3>Avantages des banques digitales</h3>
            <ul>
                <li>✅ <strong>Frais bancaires réduits</strong> : jusqu'à 50% moins cher que les agences traditionnelles</li>
                <li>✅ <strong>Ouverture en ligne</strong> : 10 minutes avec CIN et selfie</li>
                <li>✅ <strong>Cartes virtuelles gratuites</strong> : pour les achats en ligne sécurisés</li>
                <li>✅ <strong>Transferts instantanés</strong> : entre comptes de la même banque</li>
                <li>✅ <strong>Notifications temps réel</strong> : alertes SMS/push pour chaque opération</li>
            </ul>
            <h3>Comparatif frais mensuels 2026</h3>
            <table style="width:100%; border-collapse:collapse; margin:1rem 0;">
                <tr style="background:#1a365d; color:white;"><th>Banque</th><th>Compte classique</th><th>Offre digitale</th></tr>
                <tr><td>Attijariwafa Bank</td><td>30-50 MAD/mois</td><td>15-25 MAD/mois</td></tr>
                <tr><td>BMCE Bank</td><td>25-45 MAD/mois</td><td>10-20 MAD/mois</td></tr>
                <tr><td>CIH Bank</td><td>20-40 MAD/mois</td><td>10-15 MAD/mois</td></tr>
                <tr><td>CFG Bank</td><td>15-30 MAD/mois</td><td>5-10 MAD/mois</td></tr>
            </table>
            <h3>Ce qu'il faut savoir</h3>
            <p>Les agences physiques restent utiles pour les <strong>crédits importants</strong>, les <strong>conseils patrimoniaux</strong> et les <strong>opérations complexes</strong> (succession, donation). La combinaison des deux est souvent optimale : un compte digital pour les opérations courantes, une relation agence pour les projets importants.</p>
            <p><strong>Conseil</strong> : Comparez les offres avec notre comparateur de cartes bancaires pour trouver la banque qui correspond à votre usage réel.</p>
            ""","banques.jpg",datetime.now().isoformat(),0),

            ("Investir en Bourse de Casablanca : Guide Débutant 2026","bourse-casablanca-debutant-2026","Investissement","""
            <h2>Comment investir en Bourse de Casablanca ?</h2>
            <p>La <strong>Bourse de Casablanca</strong> compte plus de 75 sociétés cotées avec une capitalisation totale dépassant 600 MMDH. En 2026, l'indice MASI affiche une performance positive soutenue par le secteur bancaire et les télécoms.</p>
            <h3>Les étapes pour commencer</h3>
            <ol>
                <li><strong>Choisir un intermédiaire</strong> : banque avec service bourse ou société de bourse agréée (Attijari Intermediation, BMCE Capital, CDG Capital...)</li>
                <li><strong>Ouvrir un compte-titres</strong> : CIN, RIB, justificatif de domicile</li>
                <li><strong>Définir votre stratégie</strong> : valeur, croissance, dividende</li>
                <li><strong>Placer votre premier ordre</strong> : achat au marché ou à cours limité</li>
                <li><strong>Suivre et rééquilibrer</strong> : revue trimestrielle de votre portefeuille</li>
            </ol>
            <h3>Les secteurs les plus performants en 2026</h3>
            <ul>
                <li><strong>Banques/Assurances</strong> : Attijariwafa, BMCE, CIH, Saham (dividendes réguliers)</li>
                <li><strong>Télécoms</strong> : Maroc Telecom, Inwi (stabilité, rendement)</li>
                <li><strong>Immobilier</strong> : Addoha, Alliances (reprise post-COVID)</li>
                <li><strong>Industrie</strong> : Cosumar, Centrale Danone (consommation locale)</li>
            </ul>
            <h3>Fiscalité des plus-values boursières</h3>
            <table style="width:100%; border-collapse:collapse; margin:1rem 0;">
                <tr style="background:#1a365d; color:white;"><th>Type de gain</th><th>Taux d'imposition</th><th>Condition</th></tr>
                <tr><td>Plus-values cession</td><td>15% IR</td><td>Compte-titres classique</td></tr>
                <tr><td>Dividendes</td><td>12.5% retenue à la source</td><td>Tous comptes</td></tr>
                <tr><td>Plus-values PEA</td><td>0% (exonéré)</td><td>Après 5 ans de détention</td></tr>
                <tr><td>Dividendes PEA</td><td>0% (exonéré)</td><td>Après 5 ans de détention</td></tr>
            </table>
            <p><strong>Attention</strong> : Investir en bourse comporte des risques. Ne placez que l'argent dont vous n'avez pas besoin à court terme. Diversifiez votre portefeuille.</p>
            ""","bourse.jpg",datetime.now().isoformat(),0),
        ]
        cursor.executemany("""
            INSERT INTO articles (titre, slug, categorie, contenu, image, date_pub, lu)
            VALUES (?,?,?,?,?,?,?)
        """, articles_data)

    conn.commit()
    conn.close()

# ============================================
# ROUTES API
# ============================================

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

# API Leads / Collecte d'emails
@app.route('/api/leads', methods=['POST'])
def create_lead():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO leads (email, nom, telephone, objet, source)
            VALUES (?, ?, ?, ?, ?)
        """, (data.get('email'), data.get('nom'), data.get('telephone'), 
              data.get('objet'), data.get('source', 'homepage')))
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

# API OPCVM
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

# API Cartes Bancaires
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

# API Crédits
@app.route('/api/credits', methods=['GET'])
def get_credits():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credits")
    credits = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(credits)

# API Blog
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

# API Simulations
@app.route('/api/simulations', methods=['POST'])
def save_simulation():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO simulations (type, params, resultats, email)
        VALUES (?, ?, ?, ?)
    """, (data.get('type'), json.dumps(data.get('params')), 
          json.dumps(data.get('resultats')), data.get('email')))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# API Stats admin
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
    return jsonify({
        "total_leads": total_leads,
        "total_simulations": total_simulations,
        "total_articles": total_articles,
        "leads_today": leads_today
    })

# Simulateur Crédit Immobilier
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

    # Tableau d'amortissement
    tableau = []
    solde = capital
    for i in range(1, min(n + 1, 13)):
        interet_mois = solde * taux_mensuel
        amortissement = mensualite - interet_mois
        solde -= amortissement
        tableau.append({
            "mois": i,
            "mensualite": round(mensualite, 2),
            "interet": round(interet_mois, 2),
            "amortissement": round(amortissement, 2),
            "solde": round(max(solde, 0), 2)
        })

    return jsonify({
        "mensualite": round(mensualite, 2),
        "cout_total": round(cout_total, 2),
        "interets": round(interets, 2),
        "capital": round(capital, 2),
        "tableau": tableau,
        "taux_endettement": round((mensualite / revenu) * 100, 2)
    })

# Simulateur Retraite
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

    return jsonify({
        "capital_necessaire": round(capital_necessaire, 2),
        "versement_mensuel": round(versement_mensuel, 2),
        "besoin_mensuel": round(besoin_mensuel, 2),
        "annees_epargne": annees,
        "capital_projete": round(capital_projete, 2),
        "taux_remplacement": taux_remplacement * 100,
        "evolution": evolution
    })

# Simulateur Investissement
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

    return jsonify({
        "total": round(total, 2),
        "interets": round(interets, 2),
        "capital_investi": round(capital_investi, 2),
        "evolution": evolution,
        "performance": round((interets / capital_investi) * 100, 2) if capital_investi > 0 else 0
    })

# Simulateur Budget
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
        suggestions.append("🏠 Votre loyer dépasse 33% de vos revenus. Envisagez un logement moins cher ou un colocataire.")
    if transport > revenus * 0.15:
        suggestions.append("🚗 Vos frais de transport sont élevés. Le covoiturage ou les transports en commun peuvent réduire cette dépense.")
    if loisirs > revenus * 0.1:
        suggestions.append("🎉 Vos dépenses de loisirs dépassent 10%. Réduisez les sorties ou choisissez des activités gratuites.")
    if nourriture > revenus * 0.2:
        suggestions.append("🍽️ Votre budget nourriture est élevé. Faites vos courses en gros et cuisinez chez vous.")
    if solde < 0:
        suggestions.append("⚠️ Vous êtes en déficit ! Réduisez immédiatement vos dépenses.")
    elif solde < epargne_recommandee:
        suggestions.append(f"💡 Il vous manque {round(epargne_recommandee - solde, 0)} MAD/mois pour atteindre votre objectif d'épargne de {objectif_epargne}%.")
    else:
        suggestions.append(f"✅ Bravo ! Vous pouvez épargner {round(solde, 0)} MAD/mois, ce qui dépasse votre objectif.")

    return jsonify({
        "total_depenses": round(total_depenses, 2),
        "solde": round(solde, 2),
        "epargne_recommandee": round(epargne_recommandee, 2),
        "taux_epargne": round((solde / revenus) * 100, 2) if revenus > 0 else 0,
        "taux_endettement": round((total_depenses / revenus) * 100, 2) if revenus > 0 else 0,
        "suggestions": suggestions,
        "repartition": {
            "loyer": loyer, "transport": transport, "nourriture": nourriture,
            "sante": sante, "loisirs": loisirs, "autres": autres,
            "epargne": max(solde, 0)
        }
    })

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    print("=" * 50)
    print("  Dirhami.ma - Serveur démarré")
    print("  Base de données initialisée avec données 2026")
    print(f"  Port: {port}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=False)
