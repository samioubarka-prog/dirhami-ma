from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(50))
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    simulations = relationship("Simulation", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")

class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    type = Column(String(50), nullable=False)  # credit, retraite, budget, opcvm
    name = Column(String(255))
    data = Column(Text)  # JSON string
    result = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="simulations")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_type = Column(String(50), nullable=False)  # carte, opcvm
    item_id = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="favorites")

class CarteBancaire(Base):
    __tablename__ = "cartes_bancaires"

    id = Column(String(100), primary_key=True)
    banque = Column(String(100), nullable=False)
    nom = Column(String(255), nullable=False)
    type_carte = Column(String(50))
    categorie = Column(String(50))
    frais_annuel = Column(Float)
    frais_retrait_gab = Column(Float)
    frais_retrait_hors_gab = Column(Float)
    plafond_retrait = Column(Integer)
    plafond_paiement = Column(Integer)
    taux_change = Column(Float)
    assurance_voyage = Column(Boolean, default=False)
    cashback = Column(Float, default=0)
    avantages = Column(Text)
    url_image = Column(String(500))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class OPCVM(Base):
    __tablename__ = "opcvm"

    id = Column(String(100), primary_key=True)
    nom = Column(String(255), nullable=False)
    societe = Column(String(255))
    categorie = Column(String(100))
    type_opcvm = Column(String(50))
    rendement_1an = Column(Float)
    rendement_3ans = Column(Float)
    rendement_5ans = Column(Float)
    frais_gestion = Column(Float)
    frais_entree = Column(Float)
    frais_sortie = Column(Float)
    volatilite = Column(String(50))
    capital_minimum = Column(Integer)
    description = Column(Text)
    composition = Column(Text)
    benchmark = Column(String(100))
    url_ammc = Column(String(500))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class BlogArticle(Base):
    __tablename__ = "blog_articles"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(255), unique=True, index=True)
    titre = Column(String(500), nullable=False)
    categorie = Column(String(100))
    resume = Column(Text)
    contenu = Column(Text)
    image_url = Column(String(500))
    published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
