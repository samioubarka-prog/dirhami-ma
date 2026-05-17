from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Article
from app.schemas import ArticleOut

router = APIRouter()

DEMO_ARTICLES = [
    {
        "title": "Guide complet du credit immobilier au Maroc 2024",
        "slug": "guide-credit-immobilier-maroc",
        "excerpt": "Tout ce que vous devez savoir pour obtenir un credit immobilier au Maroc : taux, conditions, banques participatives vs conventionnelles.",
        "content": "# Guide du Credit Immobilier au Maroc\n\n## Les taux actuels (2024)\n- Taux conventionnels : 4.5% a 6.5%\n- Taux participatifs (Mourabaha) : 5% a 7%\n\n## Conditions d'eligibilite\n- Apport personnel minimum : 10-20%\n- Duree maximale : 25 ans\n- Endettement maximum : 40% des revenus\n\n## Banques participatives vs Conventionnelles\nLes banques participatives utilisent le Mourabaha (achat-revente) au lieu de l'interet classique.\n\n## Comment utiliser notre simulateur\nRendez-vous sur la page Simulateurs > Credit Immobilier pour calculer vos mensualites.",
        "category": "credit",
        "author": "Equipe Dirhami",
        "image_url": "/assets/blog/credit-immobilier.jpg"
    },
    {
        "title": "Comment investir a la Bourse de Casablanca",
        "slug": "investir-bourse-casablanca",
        "excerpt": "Decouvrez comment debuter en bourse au Maroc : SVM, OPCVM, et strategies d'investissement.",
        "content": "# Investir a la Bourse de Casablanca\n\n## Les instruments disponibles\n- **Actions**: Titres de societes cotees\n- **Obligations**: Emprunts d'Etat ou d'entreprises\n- **OPCVM**: Fonds communs de placement\n\n## Comment commencer\n1. Ouvrez un compte titres chez une banque ou un intermediaire\n2. Definissez votre profil de risque\n3. Commencez avec des montants modestes\n\n## Rendements historiques\nL'indice MASI a affiche en moyenne 8-12% de rendement annuel sur les 10 dernieres annees.",
        "category": "investissement",
        "author": "Equipe Dirhami",
        "image_url": "/assets/blog/bourse-casa.jpg"
    },
    {
        "title": "L'epargne participative : Dar Assafaa vs Umnia Bank",
        "slug": "epargne-participative-comparatif",
        "excerpt": "Comparatif des comptes d'epargne participative au Maroc sans riba.",
        "content": "# Epargne Participative au Maroc\n\n## Principes de la finance participative\n- Pas d'interet (riba)\n- Partage des profits et pertes\n- Investissement dans l'economie reelle\n\n## Comparaison des banques participatives\n\n### Umnia Bank\n- Compte d'epargne Wafir: rendement variable\n- Mourabaha immobilier\n\n### Dar Assafaa\n- Compte d'epargne participative\n- Financement conforme a la Charia\n\n## Rendements\nLes rendements sont variables et dependent des profits realises par la banque.",
        "category": "epargne",
        "author": "Equipe Dirhami",
        "image_url": "/assets/blog/epargne-participative.jpg"
    },
    {
        "title": "Assurance auto au Maroc : comment reduire votre prime",
        "slug": "assurance-auto-maroc",
        "excerpt": "Astuces pour payer moins cher votre assurance automobile au Maroc.",
        "content": "# Reduire son Assurance Auto au Maroc\n\n## Facteurs qui influencent le prix\n- **Bonus-malus**: Votre historique de sinistres\n- **Type de vehicule**: Puissance et valeur\n- **Usage**: Professionnel ou prive\n- **Zone**: Casablanca/Rabat vs provinces\n\n## Astuces pour economiser\n1. Comparez les offres (Wafir.ma, Dirhami)\n2. Augmentez votre franchise\n3. Garez votre voiture en parking securise\n4. Souscrivez en ligne pour des reductions\n\n## Prix moyens 2024\n- Citadine: 2,500 - 4,000 MAD/an\n- Berline: 4,000 - 7,000 MAD/an\n- SUV/Luxe: 7,000 - 15,000 MAD/an",
        "category": "assurance",
        "author": "Equipe Dirhami",
        "image_url": "/assets/blog/assurance-auto.jpg"
    },
    {
        "title": "Cryptomonnaies au Maroc : legalite et risques",
        "slug": "crypto-maroc-legalite",
        "excerpt": "L'etat actuel des cryptomonnaies au Maroc et les alternatives d'investissement.",
        "content": "# Cryptomonnaies au Maroc\n\n## Situation juridique\n- **2017**: Office des Changes interdit les transactions crypto\n- **2023**: Bank Al-Maghrib rappelle l'interdiction\n- **Risque**: Amendes et sanctions penales possibles\n\n## Pourquoi l'interdiction ?\n- Risque de blanchiment d'argent\n- Volatilite extreme\n- Protection des epargnants\n\n## Alternatives legales au Maroc\n1. **Bourse de Casablanca**: Actions, obligations\n2. **OPCVM**: Fonds diversifies\n3. **Or physique**: Disponible dans les banques\n4. **Immobilier**: SCPI, achat locatif\n\n## Conseil\nNe risquez pas des sanctions legales. Utilisez les instruments financiers autorises au Maroc.",
        "category": "crypto",
        "author": "Equipe Dirhami",
        "image_url": "/assets/blog/crypto-maroc.jpg"
    }
]

@router.get("/", response_model=List[ArticleOut])
async def get_articles(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    limit: int = 10,
    skip: int = 0
):
    query = db.query(Article).filter(Article.is_published == True)
    if category:
        query = query.filter(Article.category == category)

    articles = query.offset(skip).limit(limit).all()

    if not articles:
        for art in DEMO_ARTICLES:
            article = Article(**art, is_published=True)
            db.add(article)
        db.commit()
        articles = query.offset(skip).limit(limit).all()

    return articles

@router.get("/{slug}", response_model=ArticleOut)
async def get_article(slug: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(404, "Article non trouve")

    article.views += 1
    db.commit()

    return article
