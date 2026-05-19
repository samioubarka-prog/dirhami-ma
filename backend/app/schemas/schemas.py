from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

# Simulation schemas
class SimulationBase(BaseModel):
    type: str
    name: Optional[str] = None
    data: str
    result: Optional[str] = None

class SimulationCreate(SimulationBase):
    pass

class SimulationResponse(SimulationBase):
    id: int
    user_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

# Carte schemas
class CarteBancaireBase(BaseModel):
    id: str
    banque: str
    nom: str
    type_carte: Optional[str] = None
    categorie: Optional[str] = None
    frais_annuel: Optional[float] = None
    frais_retrait_gab: Optional[float] = None
    frais_retrait_hors_gab: Optional[float] = None
    plafond_retrait: Optional[int] = None
    plafond_paiement: Optional[int] = None
    taux_change: Optional[float] = None
    assurance_voyage: Optional[bool] = False
    cashback: Optional[float] = 0
    avantages: Optional[str] = None
    url_image: Optional[str] = None

class CarteBancaireResponse(CarteBancaireBase):
    class Config:
        from_attributes = True

# OPCVM schemas
class OPCVMBase(BaseModel):
    id: str
    nom: str
    societe: Optional[str] = None
    categorie: Optional[str] = None
    type_opcvm: Optional[str] = None
    rendement_1an: Optional[float] = None
    rendement_3ans: Optional[float] = None
    rendement_5ans: Optional[float] = None
    frais_gestion: Optional[float] = None
    frais_entree: Optional[float] = None
    frais_sortie: Optional[float] = None
    volatilite: Optional[str] = None
    capital_minimum: Optional[int] = None
    description: Optional[str] = None
    composition: Optional[str] = None
    benchmark: Optional[str] = None
    url_ammc: Optional[str] = None

class OPCVMResponse(OPCVMBase):
    class Config:
        from_attributes = True

# Blog schemas
class BlogArticleBase(BaseModel):
    slug: str
    titre: str
    categorie: Optional[str] = None
    resume: Optional[str] = None
    contenu: Optional[str] = None
    image_url: Optional[str] = None

class BlogArticleResponse(BlogArticleBase):
    id: int
    published: bool
    created_at: datetime

    class Config:
        from_attributes = True
