from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# ==================== UTILISATEURS ====================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    city = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    simulations = relationship("Simulation", back_populates="user")
    budgets = relationship("Budget", back_populates="user")

# ==================== CARTES BANCAIRES ====================
class BankCard(Base):
    __tablename__ = "bank_cards"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String(100), nullable=False, index=True)
    card_name = Column(String(200), nullable=False)
    card_type = Column(String(50), nullable=False)  # Visa, Mastercard, etc.
    card_category = Column(String(50))  # Classic, Gold, Platinum, Infinite

    # Frais annuels
    annual_fee_mad = Column(Float, default=0)
    annual_fee_first_year_free = Column(Boolean, default=False)

    # Retraits DAB
    withdrawal_fee_own_bank = Column(Float, default=0)
    withdrawal_fee_other_bank = Column(Float, default=0)
    withdrawal_fee_abroad = Column(Float, default=0)
    withdrawal_limit_mad = Column(Float, default=0)

    # Paiements
    payment_abroad_fee_percent = Column(Float, default=0)
    payment_online_fee_percent = Column(Float, default=0)

    # Assurance & Assistance
    travel_insurance = Column(Boolean, default=False)
    purchase_insurance = Column(Boolean, default=False)
    medical_assistance_abroad = Column(Boolean, default=False)

    # Avantages
    cashback_percent = Column(Float, default=0)
    loyalty_program = Column(String(100))
    lounge_access = Column(Boolean, default=False)

    # Conditions
    min_salary_mad = Column(Float, default=0)
    required_documents = Column(JSON, default=list)

    description = Column(Text)
    logo_url = Column(String(500))
    official_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

# ==================== CRÉDITS IMMOBILIERS ====================
class MortgageRate(Base):
    __tablename__ = "mortgage_rates"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String(100), nullable=False, index=True)
    product_name = Column(String(200), nullable=False)

    # Taux
    interest_rate_fixed = Column(Float)
    interest_rate_variable = Column(Float)
    interest_rate_mixed = Column(Float)
    taeg_min = Column(Float)
    taeg_max = Column(Float)

    # Conditions
    min_amount_mad = Column(Float, default=50000)
    max_amount_mad = Column(Float, default=5000000)
    min_duration_months = Column(Integer, default=12)
    max_duration_months = Column(Integer, default=300)
    max_financing_percent = Column(Float, default=80)

    # Frais
    application_fee_mad = Column(Float, default=0)
    file_fee_percent = Column(Float, default=0)
    notary_fee_percent = Column(Float, default=0)
    mortgage_registration_fee = Column(Float, default=0)
    early_repayment_penalty = Column(Float, default=0)

    # Assurances obligatoires
    life_insurance_required = Column(Boolean, default=True)
    life_insurance_rate = Column(Float, default=0.3)
    job_loss_insurance = Column(Boolean, default=False)

    # Conditions d'éligibilité
    min_salary_mad = Column(Float, default=3000)
    max_age_at_end = Column(Integer, default=70)
    required_employment_years = Column(Integer, default=2)

    description = Column(Text)
    logo_url = Column(String(500))
    official_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

# ==================== OPCVM (FONDS COMMUNS) ====================
class OPCVM(Base):
    __tablename__ = "opcvm"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    isin_code = Column(String(20), unique=True, index=True)

    # Société de gestion
    management_company = Column(String(200), nullable=False)
    category = Column(String(100))  # Actions, Obligations, Diversifié, Monétaire
    risk_profile = Column(String(50))  # Faible, Modéré, Élevé

    # Frais
    entry_fee_percent = Column(Float, default=0)
    exit_fee_percent = Column(Float, default=0)
    management_fee_percent = Column(Float, default=0)
    performance_fee_percent = Column(Float, default=0)

    # Performance (historique)
    ytd_return = Column(Float)
    one_year_return = Column(Float)
    three_year_return = Column(Float)
    five_year_return = Column(Float)
    since_inception_return = Column(Float)

    # Caractéristiques
    min_subscription_mad = Column(Float, default=1000)
    nav_mad = Column(Float)
    aum_mad = Column(Float)  # Actifs sous gestion
    launch_date = Column(DateTime)
    benchmark = Column(String(100))

    # Allocation
    equity_percent = Column(Float)
    bond_percent = Column(Float)
    cash_percent = Column(Float)
    other_percent = Column(Float)

    description = Column(Text)
    logo_url = Column(String(500))
    official_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

# ==================== RÉGIMES FISCAUX ====================
class TaxRegime(Base):
    __tablename__ = "tax_regimes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, index=True)

    # Type
    regime_type = Column(String(100))  # PEA, PER, Assurance Vie, etc.

    # Avantages fiscaux
    tax_deduction_percent = Column(Float, default=0)
    tax_deduction_max_mad = Column(Float, default=0)
    tax_exemption_duration_years = Column(Integer, default=0)

    # Conditions
    min_subscription_mad = Column(Float, default=0)
    max_subscription_mad = Column(Float)
    lock_up_period_years = Column(Integer, default=0)

    # Retrait
    withdrawal_conditions = Column(Text)
    early_withdrawal_penalty = Column(Text)

    # Eligibilité
    eligible_profiles = Column(JSON, default=list)  # Salarié, Indépendant, TNS
    age_requirements = Column(String(200))

    description = Column(Text)
    official_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

# ==================== SIMULATIONS (Historique utilisateur) ====================
class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    simulation_type = Column(String(50), nullable=False)  # mortgage, retirement, budget, savings

    # Données d'entrée
    input_data = Column(JSON)
    # Résultats
    result_data = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="simulations")

# ==================== BUDGETS UTILISATEUR ====================
class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(200), default="Mon Budget")

    # Revenus
    monthly_income = Column(Float, default=0)
    additional_income = Column(Float, default=0)

    # Dépenses catégorisées
    housing_expense = Column(Float, default=0)
    transport_expense = Column(Float, default=0)
    food_expense = Column(Float, default=0)
    health_expense = Column(Float, default=0)
    education_expense = Column(Float, default=0)
    leisure_expense = Column(Float, default=0)
    savings_goal = Column(Float, default=0)
    other_expenses = Column(Float, default=0)

    # Analyse
    total_expenses = Column(Float, default=0)
    remaining = Column(Float, default=0)
    savings_rate = Column(Float, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="budgets")

# ==================== ARTICLES BLOG ====================
class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    slug = Column(String(300), unique=True, index=True)
    category = Column(String(100))
    excerpt = Column(Text)
    content = Column(Text)
    image_url = Column(String(500))
    author = Column(String(100))
    tags = Column(JSON, default=list)
    views = Column(Integer, default=0)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
