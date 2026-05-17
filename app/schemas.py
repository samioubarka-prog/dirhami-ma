from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    city: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class BankOut(BaseModel):
    id: int
    name: str
    name_ar: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    type: str
    class Config:
        orm_mode = True

class ArticleOut(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: str
    content: str
    category: str
    image_url: Optional[str] = None
    author: str
    published_at: datetime
    views: int
    is_published: bool
    class Config:
        orm_mode = True

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class InvestmentCalc(BaseModel):
    initial_amount: float
    monthly_contribution: float
    annual_rate: float
    years: int
    compound_frequency: int = 12

class LoanCalc(BaseModel):
    amount: float
    rate: float
    years: int
    type: str = "amortissable"

class RetirementCalc(BaseModel):
    current_age: int
    retirement_age: int
    monthly_savings: float
    current_savings: float
    expected_return: float
