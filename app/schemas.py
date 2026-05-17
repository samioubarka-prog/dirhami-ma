from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2)
    phone: Optional[str] = None
    city: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str]
    city: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class BankBase(BaseModel):
    name: str
    name_ar: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    type: str

class BankOut(BankBase):
    id: int
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    category: str
    type: str
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    interest_rate: Optional[float] = None
    duration_months: Optional[int] = None
    fees: float = 0
    description: Optional[str] = None
    features: List[str] = []

class ProductOut(ProductBase):
    id: int
    bank_id: int
    bank: Optional[BankOut] = None
    class Config:
        orm_mode = True

class SimulationCreate(BaseModel):
    type: str
    amount: float
    duration_months: int
    monthly_contribution: float = 0
    interest_rate: float
    product_id: Optional[int] = None

class SimulationOut(BaseModel):
    id: int
    type: str
    amount: float
    duration_months: int
    monthly_contribution: float
    interest_rate: float
    total_return: float
    total_amount: float
    created_at: datetime
    class Config:
        orm_mode = True

class ArticleBase(BaseModel):
    title: str
    slug: str
    excerpt: str
    content: str
    category: str
    image_url: Optional[str] = None
    author: str

class ArticleOut(ArticleBase):
    id: int
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
