from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import OPCVM
from app.schemas.schemas import OPCVMResponse

router = APIRouter(prefix="/opcvm", tags=["opcvm"])

@router.get("/", response_model=List[OPCVMResponse])
def get_opcvm(
    categorie: Optional[str] = None,
    type_opcvm: Optional[str] = None,
    max_frais: Optional[float] = None,
    max_capital: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(OPCVM)
    if categorie:
        query = query.filter(OPCVM.categorie == categorie)
    if type_opcvm:
        query = query.filter(OPCVM.type_opcvm == type_opcvm)
    if max_frais:
        query = query.filter(OPCVM.frais_gestion <= max_frais)
    if max_capital:
        query = query.filter(OPCVM.capital_minimum <= max_capital)
    return query.all()

@router.get("/{opcvm_id}", response_model=OPCVMResponse)
def get_opcvm_detail(opcvm_id: str, db: Session = Depends(get_db)):
    opcvm = db.query(OPCVM).filter(OPCVM.id == opcvm_id).first()
    if not opcvm:
        raise HTTPException(status_code=404, detail="OPCVM non trouvé")
    return opcvm
