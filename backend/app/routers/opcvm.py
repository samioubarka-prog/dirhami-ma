from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os

from app.database import get_db
from app.schemas import OPCVMResponse, OPCVMFilter, OPCVMSimulationInput, OPCVMSimulationResult
from app.services.calculations import calculate_opcvm_simulation

router = APIRouter(prefix="/api/opcvm", tags=["OPCVM"])

DATA_PATH = os.path.join("backend", "app", "data", "opcvm.json")

def load_opcvm():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/", response_model=List[OPCVMResponse])
def get_opcvm(
    management_company: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    risk_profile: Optional[str] = Query(None),
    max_entry_fee: Optional[float] = Query(None),
    min_return_1y: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    funds = load_opcvm()
    filtered = funds
    if management_company:
        filtered = [f for f in filtered if management_company.lower() in f["management_company"].lower()]
    if category:
        filtered = [f for f in filtered if category.lower() in f["category"].lower()]
    if risk_profile:
        filtered = [f for f in filtered if f.get("risk_profile") and risk_profile.lower() in f["risk_profile"].lower()]
    if max_entry_fee is not None:
        filtered = [f for f in filtered if f["entry_fee_percent"] <= max_entry_fee]
    if min_return_1y is not None:
        filtered = [f for f in filtered if f.get("one_year_return") and f["one_year_return"] >= min_return_1y]
    return filtered

@router.get("/{fund_id}", response_model=OPCVMResponse)
def get_opcvm_fund(fund_id: int, db: Session = Depends(get_db)):
    funds = load_opcvm()
    fund = next((f for f in funds if f["id"] == fund_id), None)
    if not fund:
        raise HTTPException(status_code=404, detail="OPCVM non trouvé")
    return fund

@router.post("/simulate", response_model=OPCVMSimulationResult)
def simulate_opcvm(input_data: OPCVMSimulationInput):
    return calculate_opcvm_simulation(input_data)

@router.get("/companies/list")
def get_management_companies(db: Session = Depends(get_db)):
    funds = load_opcvm()
    companies = list(set(f["management_company"] for f in funds))
    return {"companies": sorted(companies)}

@router.get("/categories/list")
def get_categories(db: Session = Depends(get_db)):
    funds = load_opcvm()
    categories = list(set(f["category"] for f in funds))
    return {"categories": sorted(categories)}

@router.get("/compare/")
def compare_opcvm(fund_ids: str = Query(..., description="IDs des OPCVM à comparer")):
    ids = [int(x.strip()) for x in fund_ids.split(",")]
    funds = load_opcvm()
    selected = [f for f in funds if f["id"] in ids]
    if len(selected) != len(ids):
        raise HTTPException(status_code=404, detail="Certains OPCVM n'ont pas été trouvés")
    comparison = {
        "funds": selected,
        "comparison_table": {
            "Frais d'entrée": [{"fund_id": f["id"], "value": f'{f["entry_fee_percent"]}%'} for f in selected],
            "Frais de gestion": [{"fund_id": f["id"], "value": f'{f["management_fee_percent"]}%'} for f in selected],
            "Frais de sortie": [{"fund_id": f["id"], "value": f'{f["exit_fee_percent"]}%'} for f in selected],
            "Rendement YTD": [{"fund_id": f["id"], "value": f'{f.get("ytd_return", "N/A")}%'} for f in selected],
            "Rendement 1 an": [{"fund_id": f["id"], "value": f'{f.get("one_year_return", "N/A")}%'} for f in selected],
            "Rendement 3 ans": [{"fund_id": f["id"], "value": f'{f.get("three_year_return", "N/A")}%'} for f in selected],
            "Profil risque": [{"fund_id": f["id"], "value": f.get("risk_profile", "N/A")} for f in selected],
            "Min. souscription": [{"fund_id": f["id"], "value": f'{f["min_subscription_mad"]} DH'} for f in selected],
        }
    }
    return comparison
