from fastapi import APIRouter
from app.schemas import InvestmentCalc, LoanCalc, RetirementCalc

router = APIRouter()

@router.post("/investment")
async def calculate_investment(data: InvestmentCalc):
    """
    Simulateur de rendement d'investissement avec intérêts composés
    Exemple: 10,000 MAD initial + 1,000/mois à 7% pendant 10 ans = ~207,000 MAD
    """
    r = data.annual_rate / 100 / data.compound_frequency
    n = data.years * data.compound_frequency
    pmt = data.monthly_contribution

    # Montant final avec versements réguliers (formule des intérêts composés)
    if pmt > 0:
        future_value = data.initial_amount * (1 + r) ** n + \
                      pmt * ((1 + r) ** n - 1) / r
    else:
        future_value = data.initial_amount * (1 + r) ** n

    total_contributed = data.initial_amount + (pmt * n)
    total_return = future_value - total_contributed

    # Projection annuelle détaillée
    yearly_projection = []
    balance = data.initial_amount
    total_paid = data.initial_amount

    for year in range(1, data.years + 1):
        year_start = balance
        for _ in range(data.compound_frequency):
            balance = balance * (1 + r) + pmt
            total_paid += pmt

        yearly_projection.append({
            "year": year,
            "balance": round(balance, 2),
            "contributions": round(total_paid, 2),
            "returns": round(balance - total_paid, 2),
            "return_year": round(balance - year_start - (pmt * data.compound_frequency), 2)
        })

    return {
        "initial_amount": data.initial_amount,
        "monthly_contribution": data.monthly_contribution,
        "annual_rate": data.annual_rate,
        "years": data.years,
        "total_contributed": round(total_contributed, 2),
        "total_return": round(total_return, 2),
        "final_amount": round(future_value, 2),
        "return_percentage": round((total_return / total_contributed) * 100, 2) if total_contributed > 0 else 0,
        "yearly_projection": yearly_projection
    }

@router.post("/loan")
async def calculate_loan(data: LoanCalc):
    """
    Calculateur de prêt hypothécaire
    - Amortissable: mensualité fixe
    - In fine: intérêts seulement + capital à la fin
    """
    monthly_rate = data.rate / 100 / 12
    n_months = data.years * 12

    if data.type == "amortissable":
        # Formule de calcul de la mensualité fixe
        if monthly_rate > 0:
            monthly_payment = data.amount * (monthly_rate * (1 + monthly_rate) ** n_months) / \
                            ((1 + monthly_rate) ** n_months - 1)
        else:
            monthly_payment = data.amount / n_months

        # Tableau d'amortissement complet
        schedule = []
        balance = data.amount
        total_interest = 0
        total_paid = 0

        for month in range(1, n_months + 1):
            interest_payment = balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment
            total_interest += interest_payment
            total_paid += monthly_payment

            # Afficher tous les mois pour les 12 premiers, puis annuellement
            if month <= 12 or month % 12 == 0 or month == n_months:
                schedule.append({
                    "month": month,
                    "year": (month - 1) // 12 + 1,
                    "payment": round(monthly_payment, 2),
                    "principal": round(principal_payment, 2),
                    "interest": round(interest_payment, 2),
                    "balance": round(max(balance, 0), 2),
                    "total_interest": round(total_interest, 2)
                })

        return {
            "loan_amount": data.amount,
            "rate": data.rate,
            "years": data.years,
            "type": "amortissable",
            "monthly_payment": round(monthly_payment, 2),
            "total_payments": n_months,
            "total_cost": round(monthly_payment * n_months, 2),
            "total_interest": round(total_interest, 2),
            "taeg": data.rate,
            "schedule": schedule
        }
    else:
        # Prêt in fine
        monthly_interest = data.amount * monthly_rate
        return {
            "loan_amount": data.amount,
            "rate": data.rate,
            "years": data.years,
            "type": "in_fine",
            "monthly_payment": round(monthly_interest, 2),
            "final_payment": round(data.amount, 2),
            "total_cost": round(monthly_interest * n_months + data.amount, 2),
            "total_interest": round(monthly_interest * n_months, 2),
            "taeg": data.rate
        }

@router.post("/retirement")
async def calculate_retirement(data: RetirementCalc):
    """
    Simulateur de retraite
    Calcule le capital accumulé et la pension mensuelle estimée
    """
    years_to_retire = data.retirement_age - data.current_age
    months = years_to_retire * 12

    r = data.expected_return / 100 / 12

    # Capital à la retraite (formule valeur future)
    future_value = data.current_savings * (1 + r) ** months + \
                  data.monthly_savings * ((1 + r) ** months - 1) / r

    # Rente mensuelle estimée (taux de retrait 4% annuel = règle des 4%)
    monthly_pension = future_value * 0.04 / 12

    # Projection détaillée par âge
    projection = []
    balance = data.current_savings
    cumulative_savings = data.current_savings

    for age in range(data.current_age + 1, data.retirement_age + 1):
        for _ in range(12):
            balance = balance * (1 + r) + data.monthly_savings
            cumulative_savings += data.monthly_savings

        projection.append({
            "age": age,
            "balance": round(balance, 2),
            "total_saved": round(cumulative_savings, 2),
            "returns": round(balance - cumulative_savings, 2),
            "years_remaining": data.retirement_age - age
        })

    return {
        "current_age": data.current_age,
        "retirement_age": data.retirement_age,
        "years_to_retire": years_to_retire,
        "monthly_savings": data.monthly_savings,
        "current_savings": data.current_savings,
        "expected_return": data.expected_return,
        "capital_at_retirement": round(future_value, 2),
        "estimated_monthly_pension": round(monthly_pension, 2),
        "estimated_annual_pension": round(monthly_pension * 12, 2),
        "total_contributed": round(cumulative_savings, 2),
        "total_returns": round(future_value - cumulative_savings, 2),
        "projection": projection
    }
