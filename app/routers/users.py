from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User, Simulation, Favorite
from app.schemas import UserOut, SimulationOut
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/simulations", response_model=List[SimulationOut])
async def get_my_simulations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Simulation).filter(Simulation.user_id == current_user.id).all()

@router.get("/favorites")
async def get_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    favorites = db.query(Favorite).filter(Favorite.user_id == current_user.id).all()
    return favorites
