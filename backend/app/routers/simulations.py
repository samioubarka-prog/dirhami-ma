from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Simulation, User
from app.schemas.schemas import SimulationCreate, SimulationResponse
from app.routers.auth import get_current_active_user

router = APIRouter(prefix="/simulations", tags=["simulations"])

@router.post("/", response_model=SimulationResponse)
def create_simulation(
    sim: SimulationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_sim = Simulation(
        user_id=current_user.id,
        type=sim.type,
        name=sim.name,
        data=sim.data,
        result=sim.result
    )
    db.add(db_sim)
    db.commit()
    db.refresh(db_sim)
    return db_sim

@router.get("/", response_model=List[SimulationResponse])
def get_simulations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return db.query(Simulation).filter(Simulation.user_id == current_user.id).all()

@router.delete("/{sim_id}")
def delete_simulation(
    sim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    sim = db.query(Simulation).filter(Simulation.id == sim_id, Simulation.user_id == current_user.id).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation non trouvée")
    db.delete(sim)
    db.commit()
    return {"message": "Simulation supprimée"}
