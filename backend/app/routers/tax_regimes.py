from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os

from app.database import get_db
from app.schemas import TaxRegimeResponse

router = APIRouter(prefix="/api/tax-regimes", tags=["Régimes Fiscaux"])

DATA_PATH = os.path.join("backend", "app", "data", "tax_regimes.json")

def load_tax_regimes():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/", response_model=List[TaxRegimeResponse])
def get_tax_regimes(
    regime_type: Optional[str] = Query(None),
    eligible_profile: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    regimes = load_tax_regimes()
    filtered = regimes
    if regime_type:
        filtered = [r for r in filtered if regime_type.lower() in r.get("regime_type", "").lower()]
    if eligible_profile:
        filtered = [r for r in filtered if r.get("eligible_profiles") and 
                   any(eligible_profile.lower() in p.lower() for p in r["eligible_profiles"])]
    return filtered

@router.get("/{regime_id}", response_model=TaxRegimeResponse)
def get_tax_regime(regime_id: int, db: Session = Depends(get_db)):
    regimes = load_tax_regimes()
    regime = next((r for r in regimes if r["id"] == regime_id), None)
    if not regime:
        raise HTTPException(status_code=404, detail="Régime fiscal non trouvé")
    return regime

@router.get("/types/list")
def get_regime_types(db: Session = Depends(get_db)):
    regimes = load_tax_regimes()
    types = list(set(r["regime_type"] for r in regimes if r.get("regime_type")))
    return {"types": sorted(types)}

@router.get("/calculator/deduction")
def calculate_tax_deduction(
    regime_code: str = Query(..., description="Code du régime"),
    amount: float = Query(..., gt=0, description="Montant concerné"),
    annual_income: float = Query(..., gt=0, description="Revenu annuel brut")
):
    regimes = load_tax_regimes()
    regime = next((r for r in regimes if r["code"] == regime_code), None)
    if not regime:
        raise HTTPException(status_code=404, detail="Régime fiscal non trouvé")

    deduction_percent = regime["tax_deduction_percent"]
    max_deduction = regime["tax_deduction_max_mad"]

    calculated_deduction = amount * (deduction_percent / 100)
    actual_deduction = min(calculated_deduction, max_deduction) if max_deduction > 0 else calculated_deduction
    tax_savings = actual_deduction * 0.30

    return {
        "regime": regime,
        "amount": amount,
        "deduction_percent": deduction_percent,
        "calculated_deduction": round(calculated_deduction, 2),
        "max_deduction": max_deduction,
        "actual_deduction": round(actual_deduction, 2),
        "tax_savings": round(tax_savings, 2),
        "effective_return": round((tax_savings / amount * 100), 2) if amount > 0 else 0
    }
