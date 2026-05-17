from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import BankProduct

router = APIRouter()

@router.get("/products")
async def get_loan_products(db: Session = Depends(get_db), type: str = None):
    query = db.query(BankProduct).filter(BankProduct.category == "credit")
    if type:
        query = query.filter(BankProduct.type == type)
    return query.all()

@router.get("/types")
async def get_loan_types():
    return {
        "types": [
            {"id": "immobilier", "name": "Credit Immobilier", "rate_range": "4.5% - 6.5%", "duration": "7-25 ans"},
            {"id": "auto", "name": "Credit Auto", "rate_range": "5% - 8%", "duration": "1-7 ans"},
            {"id": "conso", "name": "Credit Consommation", "rate_range": "6% - 10%", "duration": "1-5 ans"},
            {"id": "renouvelable", "name": "Credit Renouvelable", "rate_range": "8% - 12%", "duration": "1-3 ans"},
            {"id": "etudiant", "name": "Pret Etudiant", "rate_range": "3% - 5%", "duration": "1-8 ans"}
        ]
    }
