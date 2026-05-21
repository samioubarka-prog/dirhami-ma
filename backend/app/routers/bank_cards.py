from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os

from app.database import get_db
from app.schemas import BankCardResponse, BankCardFilter

router = APIRouter(prefix="/api/bank-cards", tags=["Cartes Bancaires"])

# Chemin depuis la racine du projet (Render working directory)
DATA_PATH = os.path.join("backend", "app", "data", "bank_cards.json")

def load_bank_cards():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/", response_model=List[BankCardResponse])
def get_bank_cards(
    bank_name: Optional[str] = Query(None, description="Filtrer par banque"),
    card_type: Optional[str] = Query(None, description="Filtrer par type (Visa, Mastercard)"),
    card_category: Optional[str] = Query(None, description="Filtrer par catégorie (Classic, Gold, Platinum)"),
    max_annual_fee: Optional[float] = Query(None, description="Frais annuels maximum"),
    has_travel_insurance: Optional[bool] = Query(None, description="Avec assurance voyage"),
    has_cashback: Optional[bool] = Query(None, description="Avec cashback"),
    db: Session = Depends(get_db)
):
    cards = load_bank_cards()
    filtered = cards
    if bank_name:
        filtered = [c for c in filtered if bank_name.lower() in c["bank_name"].lower()]
    if card_type:
        filtered = [c for c in filtered if card_type.lower() in c["card_type"].lower()]
    if card_category:
        filtered = [c for c in filtered if c.get("card_category") and card_category.lower() in c["card_category"].lower()]
    if max_annual_fee is not None:
        filtered = [c for c in filtered if c["annual_fee_mad"] <= max_annual_fee]
    if has_travel_insurance is not None:
        filtered = [c for c in filtered if c["travel_insurance"] == has_travel_insurance]
    if has_cashback is not None:
        filtered = [c for c in filtered if (c["cashback_percent"] > 0) == has_cashback]
    return filtered

@router.get("/{card_id}", response_model=BankCardResponse)
def get_bank_card(card_id: int, db: Session = Depends(get_db)):
    cards = load_bank_cards()
    card = next((c for c in cards if c["id"] == card_id), None)
    if not card:
        raise HTTPException(status_code=404, detail="Carte bancaire non trouvée")
    return card

@router.get("/banks/list")
def get_banks_list(db: Session = Depends(get_db)):
    cards = load_bank_cards()
    banks = list(set(c["bank_name"] for c in cards))
    return {"banks": sorted(banks)}

@router.get("/compare/")
def compare_cards(card_ids: str = Query(..., description="IDs des cartes à comparer séparés par des virgules")):
    ids = [int(x.strip()) for x in card_ids.split(",")]
    cards = load_bank_cards()
    selected = [c for c in cards if c["id"] in ids]
    if len(selected) != len(ids):
        raise HTTPException(status_code=404, detail="Certaines cartes n'ont pas été trouvées")
    comparison = {
        "cards": selected,
        "comparison_table": {
            "Frais annuels": [{"card_id": c["id"], "value": f'{c["annual_fee_mad"]} DH'} for c in selected],
            "Retrait propre DAB": [{"card_id": c["id"], "value": f'{c["withdrawal_fee_own_bank"]} DH'} for c in selected],
            "Retrait autre DAB": [{"card_id": c["id"], "value": f'{c["withdrawal_fee_other_bank"]} DH'} for c in selected],
            "Retrait à l'étranger": [{"card_id": c["id"], "value": f'{c["withdrawal_fee_abroad"]} DH'} for c in selected],
            "Paiement à l'étranger": [{"card_id": c["id"], "value": f'{c["payment_abroad_fee_percent"]}%'} for c in selected],
            "Assurance voyage": [{"card_id": c["id"], "value": "Oui" if c["travel_insurance"] else "Non"} for c in selected],
            "Assistance médicale": [{"card_id": c["id"], "value": "Oui" if c["medical_assistance_abroad"] else "Non"} for c in selected],
            "Cashback": [{"card_id": c["id"], "value": f'{c["cashback_percent"]}%'} for c in selected],
            "Accès salon": [{"card_id": c["id"], "value": "Oui" if c["lounge_access"] else "Non"} for c in selected],
            "Salaire minimum": [{"card_id": c["id"], "value": f'{c["min_salary_mad"]} DH'} for c in selected],
        }
    }
    return comparison
