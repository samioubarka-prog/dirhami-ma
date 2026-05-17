from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import BankProduct

router = APIRouter()

@router.get("/products")
async def get_investment_products(db: Session = Depends(get_db)):
    products = db.query(BankProduct).filter(
        BankProduct.category == "investissement",
        BankProduct.is_active == True
    ).all()
    return products

@router.get("/categories")
async def get_categories():
    return {
        "categories": [
            {"id": "actions", "name": "Actions Bourse de Casablanca", "risk": "Eleve", "return": "8-15%"},
            {"id": "obligations", "name": "Obligations/Tresorerie", "risk": "Faible", "return": "3-5%"},
            {"id": "opcvm", "name": "OPCVM (SICAV/FCP)", "risk": "Moyen", "return": "5-10%"},
            {"id": "immobilier", "name": "SCPI / Immobilier", "risk": "Moyen", "return": "4-7%"},
            {"id": "or", "name": "Or physique", "risk": "Moyen", "return": "Variable"},
            {"id": "crypto", "name": "Cryptomonnaies", "risk": "Tres eleve", "return": "Tres variable"}
        ]
    }
