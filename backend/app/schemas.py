from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==================== AUTH ====================
class UserCreate(BaseModel):
    email: str
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    phone: Optional[str]
    city: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ==================== CARTES BANCAIRES ====================
class BankCardBase(BaseModel):
    bank_name: str
    card_name: str
    card_type: str
    card_category: Optional[str] = None
    annual_fee_mad: float = 0
    annual_fee_first_year_free: bool = False
    withdrawal_fee_own_bank: float = 0
    withdrawal_fee_other_bank: float = 0
    withdrawal_fee_abroad: float = 0
    withdrawal_limit_mad: float = 0
    payment_abroad_fee_percent: float = 0
    payment_online_fee_percent: float = 0
    travel_insurance: bool = False
    purchase_insurance: bool = False
    medical_assistance_abroad: bool = False
    cashback_percent: float = 0
    loyalty_program: Optional[str] = None
    lounge_access: bool = False
    min_salary_mad: float = 0
    required_documents: Optional[List[str]] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    official_url: Optional[str] = None

class BankCardCreate(BankCardBase):
    pass

class BankCardResponse(BankCardBase):
    id: int
    is_active: bool
    updated_at: datetime

    class Config:
        from_attributes = True

class BankCardFilter(BaseModel):
    bank_name: Optional[str] = None
    card_type: Optional[str] = None
    card_category: Optional[str] = None
    max_annual_fee: Optional[float] = None
    has_travel_insurance: Optional[bool] = None
    has_cashback: Optional[bool] = None

# ==================== CRÉDITS IMMOBILIERS ====================
class MortgageRateBase(BaseModel):
    bank_name: str
    product_name: str
    interest_rate_fixed: Optional[float] = None
    interest_rate_variable: Optional[float] = None
    interest_rate_mixed: Optional[float] = None
    taeg_min: Optional[float] = None
    taeg_max: Optional[float] = None
    min_amount_mad: float = 50000
    max_amount_mad: float = 5000000
    min_duration_months: int = 12
    max_duration_months: int = 300
    max_financing_percent: float = 80
    application_fee_mad: float = 0
    file_fee_percent: float = 0
    notary_fee_percent: float = 0
    mortgage_registration_fee: float = 0
    early_repayment_penalty: float = 0
    life_insurance_required: bool = True
    life_insurance_rate: float = 0.3
    job_loss_insurance: bool = False
    min_salary_mad: float = 3000
    max_age_at_end: int = 70
    required_employment_years: int = 2
    description: Optional[str] = None
    logo_url: Optional[str] = None
    official_url: Optional[str] = None

class MortgageRateCreate(MortgageRateBase):
    pass

class MortgageRateResponse(MortgageRateBase):
    id: int
    is_active: bool
    updated_at: datetime

    class Config:
        from_attributes = True

# ==================== SIMULATION CRÉDIT ====================
class MortgageSimulationInput(BaseModel):
    property_price: float = Field(..., gt=0, description="Prix du bien immobilier en MAD")
    down_payment_percent: float = Field(..., ge=0, le=100, description="Apport personnel en %")
    duration_years: int = Field(..., ge=1, le=30, description="Durée en années")
    interest_rate: float = Field(..., ge=0, le=20, description="Taux d'intérêt annuel en %")
    insurance_rate: float = Field(0.3, ge=0, le=2, description="Taux assurance décès en %")
    income: float = Field(..., gt=0, description="Revenu mensuel net en MAD")

class MortgageSimulationResult(BaseModel):
    loan_amount: float
    down_payment_amount: float
    monthly_payment: float
    total_interest: float
    total_cost: float
    taeg: float
    debt_ratio: float
    insurance_monthly: float
    amortization_schedule: List[dict]
    is_eligible: bool
    eligibility_reason: Optional[str] = None

# ==================== OPCVM ====================
class OPCVMBase(BaseModel):
    name: str
    isin_code: str
    management_company: str
    category: Optional[str] = None
    risk_profile: Optional[str] = None
    entry_fee_percent: float = 0
    exit_fee_percent: float = 0
    management_fee_percent: float = 0
    performance_fee_percent: float = 0
    ytd_return: Optional[float] = None
    one_year_return: Optional[float] = None
    three_year_return: Optional[float] = None
    five_year_return: Optional[float] = None
    since_inception_return: Optional[float] = None
    min_subscription_mad: float = 1000
    nav_mad: Optional[float] = None
    aum_mad: Optional[float] = None
    launch_date: Optional[datetime] = None
    benchmark: Optional[str] = None
    equity_percent: Optional[float] = None
    bond_percent: Optional[float] = None
    cash_percent: Optional[float] = None
    other_percent: Optional[float] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    official_url: Optional[str] = None

class OPCVMCreate(OPCVMBase):
    pass

class OPCVMResponse(OPCVMBase):
    id: int
    is_active: bool
    updated_at: datetime

    class Config:
        from_attributes = True

class OPCVMFilter(BaseModel):
    management_company: Optional[str] = None
    category: Optional[str] = None
    risk_profile: Optional[str] = None
    max_entry_fee: Optional[float] = None
    min_return_1y: Optional[float] = None

# ==================== SIMULATION OPCVM ====================
class OPCVMSimulationInput(BaseModel):
    initial_amount: float = Field(..., gt=0, description="Montant initial en MAD")
    monthly_contribution: float = Field(0, ge=0, description="Versement mensuel en MAD")
    duration_years: int = Field(..., ge=1, le=40, description="Durée en années")
    expected_return_percent: float = Field(..., ge=-10, le=20, description="Rendement attendu annuel en %")
    entry_fee_percent: float = Field(0, ge=0, le=5)
    management_fee_percent: float = Field(0, ge=0, le=5)
    exit_fee_percent: float = Field(0, ge=0, le=5)

class OPCVMSimulationResult(BaseModel):
    total_invested: float
    gross_value: float
    net_value: float
    total_fees: float
    total_return: float
    annualized_return: float
    yearly_breakdown: List[dict]

# ==================== RÉGIMES FISCAUX ====================
class TaxRegimeBase(BaseModel):
    name: str
    code: str
    regime_type: Optional[str] = None
    tax_deduction_percent: float = 0
    tax_deduction_max_mad: float = 0
    tax_exemption_duration_years: int = 0
    min_subscription_mad: float = 0
    max_subscription_mad: Optional[float] = None
    lock_up_period_years: int = 0
    withdrawal_conditions: Optional[str] = None
    early_withdrawal_penalty: Optional[str] = None
    eligible_profiles: Optional[List[str]] = None
    age_requirements: Optional[str] = None
    description: Optional[str] = None
    official_url: Optional[str] = None

class TaxRegimeCreate(TaxRegimeBase):
    pass

class TaxRegimeResponse(TaxRegimeBase):
    id: int
    is_active: bool
    updated_at: datetime

    class Config:
        from_attributes = True

# ==================== SIMULATION RETRAITE ====================
class RetirementSimulationInput(BaseModel):
    current_age: int = Field(..., ge=18, le=70)
    retirement_age: int = Field(..., ge=50, le=80)
    current_salary_mad: float = Field(..., gt=0)
    current_savings_mad: float = Field(0, ge=0)
    monthly_contribution_mad: float = Field(..., ge=0)
    expected_return_percent: float = Field(5, ge=0, le=15)
    inflation_rate: float = Field(2, ge=0, le=10)
    desired_pension_percent: float = Field(70, ge=0, le=100)
    life_expectancy: int = Field(85, ge=60, le=110)

class RetirementSimulationResult(BaseModel):
    years_to_retirement: int
    total_accumulated: float
    monthly_pension: float
    pension_gap: float
    replacement_rate: float
    is_on_track: bool
    recommended_contribution: float
    yearly_breakdown: List[dict]

# ==================== BUDGET ====================
class BudgetBase(BaseModel):
    name: Optional[str] = "Mon Budget"
    monthly_income: float = 0
    additional_income: float = 0
    housing_expense: float = 0
    transport_expense: float = 0
    food_expense: float = 0
    health_expense: float = 0
    education_expense: float = 0
    leisure_expense: float = 0
    savings_goal: float = 0
    other_expenses: float = 0

class BudgetCreate(BudgetBase):
    pass

class BudgetResponse(BudgetBase):
    id: int
    user_id: int
    total_expenses: float
    remaining: float
    savings_rate: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BudgetAnalysis(BaseModel):
    total_income: float
    total_expenses: float
    remaining: float
    savings_rate: float
    expense_breakdown: List[dict]
    recommendations: List[str]
    savings_potential: List[dict]

# ==================== ARTICLES ====================
class ArticleBase(BaseModel):
    title: str
    slug: str
    category: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[List[str]] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int
    views: int
    is_published: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
