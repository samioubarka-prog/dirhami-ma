from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import CarteBancaire
from app.schemas.schemas import CarteBancaireResponse

router = APIRouter(prefix="/cartes", tags=["cartes"])

@router.get("/", response_model=List[CarteBancaireResponse])
def get_cartes(
    banque: Optional[str] = None,
    type_carte: Optional[str] = None,
    categorie: Optional[str] = None,
    max_frais: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(CarteBancaire)
    if banque:
        query = query.filter(CarteBancaire.banque == banque)
    if type_carte:
        query = query.filter(CarteBancaire.type_carte == type_carte)
    if categorie:
        query = query.filter(CarteBancaire.categorie == categorie)
    if max_frais:
        query = query.filter(CarteBancaire.frais_annuel <= max_frais)
    return query.all()

@router.get("/{carte_id}", response_model=CarteBancaireResponse)
def get_carte(carte_id: str, db: Session = Depends(get_db)):
    carte = db.query(CarteBancaire).filter(CarteBancaire.id == carte_id).first()
    if not carte:
        raise HTTPException(status_code=404, detail="Carte non trouvée")
    return carte

@router.get("/banques/list")
def get_banques(db: Session = Depends(get_db)):
    banques = db.query(CarteBancaire.banque).distinct().all()
    return [b[0] for b in banques]
