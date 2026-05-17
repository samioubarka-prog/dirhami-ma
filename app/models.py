from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255))
    phone = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    role = Column(String(20), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    simulations = relationship("Simulation", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")

class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    name_ar = Column(String(255), nullable=True)
    logo_url = Column(String(500), nullable=True)
    website = Column(String(255), nullable=True)
    type = Column(String(50))
    is_active = Column(Boolean, default=True)

    products = relationship("BankProduct", back_populates="bank")

class BankProduct(Base):
    __tablename__ = "bank_products"

    id = Column(Integer, primary_key=True, index=True)
    bank_id = Column(Integer, ForeignKey("banks.id"))
    name = Column(String(255))
    category = Column(String(50))
    type = Column(String(50))
    min_amount = Column(Float, nullable=True)
    max_amount = Column(Float, nullable=True)
    interest_rate = Column(Float, nullable=True)
    duration_months = Column(Integer, nullable=True)
    fees = Column(Float, default=0)
    description = Column(Text, nullable=True)
    features = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)

    bank = relationship("Bank", back_populates="products")
    simulations = relationship("Simulation", back_populates="product")

class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("bank_products.id"), nullable=True)
    type = Column(String(50))
    amount = Column(Float)
    duration_months = Column(Integer)
    monthly_contribution = Column(Float, default=0)
    interest_rate = Column(Float)
    total_return = Column(Float)
    total_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="simulations")
    product = relationship("BankProduct", back_populates="simulations")

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    slug = Column(String(255), unique=True, index=True)
    excerpt = Column(Text)
    content = Column(Text)
    category = Column(String(50))
    image_url = Column(String(500), nullable=True)
    author = Column(String(100))
    published_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=False)
    views = Column(Integer, default=0)

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("bank_products.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    subject = Column(String(255))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
