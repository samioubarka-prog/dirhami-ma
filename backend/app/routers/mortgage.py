from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os

from app.database import get_db
from app.schemas import MortgageRateResponse, MortgageSimulationInput, MortgageSimulationResult
from app.services.calculations import calculate_mortgage_simulation

router = APIRouter(prefix="/api/mortgage", tags=["Crédits Immobiliers"])

DATA_PATH = os.path.join("backend", "app", "data", "mortgage_rates.json")

def load_mortgage_rates():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/rates", response_model=List[MortgageRateResponse])
def get_mortgage_rates(
    bank_name: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_taeg: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    rates = load_mortgage_rates()
    filtered = rates
    if bank_name:
        filtered = [r for r in filtered if bank_name.lower() in r["bank_name"].lower()]
    if min_amount:
        filtered = [r for r in filtered if r["max_amount_mad"] >= min_amount]
    if max_taeg:
        filtered = [r for r in filtered if r["taeg_min"] <= max_taeg]
    return filtered

@router.get("/rates/{rate_id}", response_model=MortgageRateResponse)
def get_mortgage_rate(rate_id: int, db: Session = Depends(get_db)):
    rates = load_mortgage_rates()
    rate = next((r for r in rates if r["id"] == rate_id), None)
    if not rate:
        raise HTTPException(status_code=404, detail="Taux non trouvé")
    return rate

@router.post("/simulate", response_model=MortgageSimulationResult)
def simulate_mortgage(input_data: MortgageSimulationInput):
    return calculate_mortgage_simulation(input_data)

@router.get("/banks/list")
def get_mortgage_banks(db: Session = Depends(get_db)):
    rates = load_mortgage_rates()
    banks = list(set(r["bank_name"] for r in rates))
    return {"banks": sorted(banks)}

@router.get("/compare/")
def compare_mortgage_rates(bank_names: str = Query(..., description="Noms des banques à comparer")):
    names = [n.strip() for n in bank_names.split(",")]
    rates = load_mortgage_rates()
    selected = [r for r in rates if any(name.lower() in r["bank_name"].lower() for name in names)]
    comparison = {
        "rates": selected,
        "comparison_table": {
            "TAEG minimum": [{"bank": r["bank_name"], "value": f'{r["taeg_min"]}%'} for r in selected],
            "TAEG maximum": [{"bank": r["bank_name"], "value": f'{r["taeg_max"]}%'} for r in selected],
            "Taux assurance": [{"bank": r["bank_name"], "value": f'{r["life_insurance_rate"]}%'} for r in selected],
            "Frais dossier": [{"bank": r["bank_name"], "value": f'{r["application_fee_mad"]} DH'} for r in selected],
            "Salaire minimum": [{"bank": r["bank_name"], "value": f'{r["min_salary_mad"]} DH'} for r in selected],
            "Âge max fin": [{"bank": r["bank_name"], "value": f'{r["max_age_at_end"]} ans'} for r in selected],
        }
    }
    return comparison
