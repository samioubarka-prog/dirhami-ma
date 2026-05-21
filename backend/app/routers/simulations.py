from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import (
    RetirementSimulationInput, RetirementSimulationResult,
    BudgetCreate, BudgetResponse, BudgetAnalysis,
    Simulation
)
from app.services.calculations import calculate_retirement_simulation, analyze_budget

router = APIRouter(prefix="/api/simulations", tags=["Simulations"])

@router.post("/retirement", response_model=RetirementSimulationResult)
def simulate_retirement(input_data: RetirementSimulationInput):
    """
    Simule la planification de la retraite
    """
    return calculate_retirement_simulation(input_data)

@router.post("/budget/analyze", response_model=BudgetAnalysis)
def analyze_budget_endpoint(budget_data: dict):
    """
    Analyse un budget et donne des recommandations
    """
    return analyze_budget(budget_data)

@router.get("/types")
def get_simulation_types():
    """
    Liste des types de simulations disponibles
    """
    return {
        "types": [
            {"id": "mortgage", "name": "Crédit Immobilier", "description": "Calculez vos mensualités et tableau d'amortissement"},
            {"id": "opcvm", "name": "Investissement OPCVM", "description": "Simulez la croissance de votre investissement"},
            {"id": "retirement", "name": "Planification Retraite", "description": "Planifiez votre retraite et vérifiez si vous êtes sur la bonne voie"},
            {"id": "budget", "name": "Analyse Budget", "description": "Analysez votre budget et trouvez des opportunités d'épargne"}
        ]
    }
