from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Bank, BankProduct
from app.schemas import BankOut, ProductOut

router = APIRouter()

BANKS_DATA = [
    {"name": "Attijariwafa Bank", "name_ar": "اتجاري وفا بنك", "type": "conventionnelle", "website": "attijariwafabank.com"},
    {"name": "BMCE Bank", "name_ar": "بنك المغرب للتجارة الخارجية", "type": "conventionnelle", "website": "bmcebank.ma"},
    {"name": "Banque Populaire", "name_ar": "البنك الشعبي", "type": "conventionnelle", "website": "bpnet.ma"},
    {"name": "CIH Bank", "name_ar": "البنك التجاري والصناعي", "type": "conventionnelle", "website": "cihbank.ma"},
    {"name": "Crédit Agricole", "name_ar": "القرض الفلاحي", "type": "conventionnelle", "website": "creditagricole.ma"},
    {"name": "Société Générale", "name_ar": "سوسيتيه جنرال", "type": "conventionnelle", "website": "sgmaroc.com"},
    {"name": "CFG Bank", "name_ar": "سي أف جي بنك", "type": "conventionnelle", "website": "cfgbank.ma"},
    {"name": "Umnia Bank", "name_ar": "أمنية بنك", "type": "participative", "website": "umniabank.com"},
    {"name": "Dar Assafaa", "name_ar": "دار الصفاء", "type": "participative", "website": "darassafaa.ma"},
    {"name": "Al Barid Bank", "name_ar": "البريد بنك", "type": "conventionnelle", "website": "albaridbank.ma"},
]

@router.get("/", response_model=List[BankOut])
async def get_banks(db: Session = Depends(get_db), type: Optional[str] = None):
    query = db.query(Bank)
    if type:
        query = query.filter(Bank.type == type)
    banks = query.all()

    if not banks:
        for bank_data in BANKS_DATA:
            bank = Bank(**bank_data)
            db.add(bank)
        db.commit()
        banks = db.query(Bank).all()

    return banks

@router.get("/{bank_id}/products", response_model=List[ProductOut])
async def get_bank_products(bank_id: int, category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(BankProduct).filter(BankProduct.bank_id == bank_id)
    if category:
        query = query.filter(BankProduct.category == category)
    return query.all()
