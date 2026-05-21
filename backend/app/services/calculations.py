import math
from typing import List, Dict, Any
from app.schemas import (
    MortgageSimulationInput, MortgageSimulationResult,
    OPCVMSimulationInput, OPCVMSimulationResult,
    RetirementSimulationInput, RetirementSimulationResult,
    BudgetAnalysis
)

# ==================== SIMULATEUR CRÉDIT IMMOBILIER ====================
def calculate_mortgage_simulation(input_data: MortgageSimulationInput) -> MortgageSimulationResult:
    """
    Calcule un crédit immobilier complet avec tableau d'amortissement
    """
    # Montant emprunté
    loan_amount = input_data.property_price * (1 - input_data.down_payment_percent / 100)
    down_payment = input_data.property_price - loan_amount

    # Paramètres
    duration_months = input_data.duration_years * 12
    monthly_rate = input_data.interest_rate / 100 / 12

    # Mensualité (formule de l'annuité)
    if monthly_rate > 0:
        monthly_payment = loan_amount * (monthly_rate * math.pow(1 + monthly_rate, duration_months)) /                          (math.pow(1 + monthly_rate, duration_months) - 1)
    else:
        monthly_payment = loan_amount / duration_months

    # Assurance décès mensuelle
    insurance_monthly = loan_amount * (input_data.insurance_rate / 100) / 12

    # Mensualité totale
    total_monthly = monthly_payment + insurance_monthly

    # Taux d'endettement
    debt_ratio = (total_monthly / input_data.income) * 100

    # Tableau d'amortissement
    amortization_schedule = []
    remaining_balance = loan_amount
    total_interest = 0

    for month in range(1, duration_months + 1):
        interest_payment = remaining_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        total_interest += interest_payment

        if remaining_balance < 0:
            remaining_balance = 0

        # Affichage annuel uniquement
        if month % 12 == 0 or month == 1:
            amortization_schedule.append({
                "month": month,
                "year": math.ceil(month / 12),
                "monthly_payment": round(monthly_payment, 2),
                "principal": round(principal_payment, 2),
                "interest": round(interest_payment, 2),
                "insurance": round(insurance_monthly, 2),
                "total_payment": round(total_monthly, 2),
                "remaining_balance": round(max(remaining_balance, 0), 2)
            })

    # Coût total du crédit
    total_cost = (monthly_payment * duration_months) + (insurance_monthly * duration_months)

    # TAEG approximatif (simplifié)
    taeg = input_data.interest_rate + (input_data.insurance_rate * 0.5)

    # Éligibilité
    is_eligible = debt_ratio <= 50
    eligibility_reason = None
    if debt_ratio > 50:
        eligibility_reason = f"Taux d'endettement de {debt_ratio:.1f}% dépasse le plafond de 50%"
    elif debt_ratio > 45 and input_data.income <= 20000:
        eligibility_reason = f"Taux d'endettement de {debt_ratio:.1f}% dépasse le plafond de 45% pour les revenus ≤ 20 000 DH"
        is_eligible = False

    return MortgageSimulationResult(
        loan_amount=round(loan_amount, 2),
        down_payment_amount=round(down_payment, 2),
        monthly_payment=round(monthly_payment, 2),
        total_interest=round(total_interest, 2),
        total_cost=round(total_cost, 2),
        taeg=round(taeg, 2),
        debt_ratio=round(debt_ratio, 2),
        insurance_monthly=round(insurance_monthly, 2),
        amortization_schedule=amortization_schedule,
        is_eligible=is_eligible,
        eligibility_reason=eligibility_reason
    )

# ==================== SIMULATEUR OPCVM ====================
def calculate_opcvm_simulation(input_data: OPCVMSimulationInput) -> OPCVMSimulationResult:
    """
    Simule l'évolution d'un investissement OPCVM avec frais
    """
    initial_amount = input_data.initial_amount
    monthly_contribution = input_data.monthly_contribution
    duration_years = input_data.duration_years
    annual_return = input_data.expected_return_percent / 100
    monthly_return = annual_return / 12

    # Frais
    entry_fee = initial_amount * (input_data.entry_fee_percent / 100)
    initial_invested = initial_amount - entry_fee

    # Frais de gestion mensuel (déduits de la performance)
    monthly_mgmt_fee = input_data.management_fee_percent / 100 / 12

    # Simulation mensuelle
    current_value = initial_invested
    total_contributed = initial_amount
    yearly_breakdown = []

    for year in range(1, duration_years + 1):
        for month in range(1, 13):
            # Versement mensuel
            if month == 1 and year > 1:  # Versement annuel pour simplifier
                current_value += monthly_contribution * 12
                total_contributed += monthly_contribution * 12

            # Rendement mensuel net de frais
            net_monthly_return = monthly_return - monthly_mgmt_fee
            current_value *= (1 + net_monthly_return)

        yearly_breakdown.append({
            "year": year,
            "value": round(current_value, 2),
            "contributed": round(total_contributed, 2),
            "gain": round(current_value - total_contributed, 2)
        })

    # Frais de sortie
    exit_fee = current_value * (input_data.exit_fee_percent / 100)
    net_value = current_value - exit_fee

    total_fees = entry_fee + (current_value * (1 - (1 - monthly_mgmt_fee) ** (duration_years * 12))) + exit_fee
    total_return = net_value - total_contributed

    # Rendement annualisé
    if total_contributed > 0 and duration_years > 0:
        annualized_return = ((net_value / total_contributed) ** (1 / duration_years) - 1) * 100
    else:
        annualized_return = 0

    return OPCVMSimulationResult(
        total_invested=round(total_contributed, 2),
        gross_value=round(current_value, 2),
        net_value=round(net_value, 2),
        total_fees=round(total_fees, 2),
        total_return=round(total_return, 2),
        annualized_return=round(annualized_return, 2),
        yearly_breakdown=yearly_breakdown
    )

# ==================== SIMULATEUR RETRAITE ====================
def calculate_retirement_simulation(input_data: RetirementSimulationInput) -> RetirementSimulationResult:
    """
    Simule la planification de la retraite
    """
    years_to_retirement = input_data.retirement_age - input_data.current_age
    remaining_years = input_data.life_expectancy - input_data.retirement_age

    # Inflation ajustée
    real_return = (input_data.expected_return_percent / 100) - (input_data.inflation_rate / 100)
    monthly_real_return = real_return / 12

    # Capital accumulé
    current_savings = input_data.current_savings_mad
    monthly_contribution = input_data.monthly_contribution_mad

    # Projection annuelle
    yearly_breakdown = []
    for year in range(1, years_to_retirement + 1):
        for month in range(1, 13):
            current_savings = current_savings * (1 + monthly_real_return) + monthly_contribution

        # Salaire ajusté à l'inflation
        adjusted_salary = input_data.current_salary_mad * math.pow(1 + input_data.inflation_rate / 100, year)

        yearly_breakdown.append({
            "year": input_data.current_age + year,
            "age": input_data.current_age + year,
            "accumulated": round(current_savings, 2),
            "annual_contribution": round(monthly_contribution * 12, 2),
            "projected_salary": round(adjusted_salary, 2)
        })

    total_accumulated = current_savings

    # Pension mensuelle (méthode du capital divisé par les années restantes avec rendement)
    if remaining_years > 0 and real_return > 0:
        monthly_pension = total_accumulated * (monthly_real_return * math.pow(1 + monthly_real_return, remaining_years * 12)) /                          (math.pow(1 + monthly_real_return, remaining_years * 12) - 1)
    else:
        monthly_pension = total_accumulated / (remaining_years * 12) if remaining_years > 0 else 0

    # Pension souhaitée (taux de remplacement)
    desired_pension = input_data.current_salary_mad * (input_data.desired_pension_percent / 100)

    # Écart
    pension_gap = desired_pension - monthly_pension
    replacement_rate = (monthly_pension / input_data.current_salary_mad) * 100 if input_data.current_salary_mad > 0 else 0

    # Sur la bonne voie ?
    is_on_track = monthly_pension >= desired_pension

    # Contribution recommandée pour atteindre l'objectif
    if pension_gap > 0 and years_to_retirement > 0 and real_return > 0:
        n_months = years_to_retirement * 12
        recommended_contribution = pension_gap * (math.pow(1 + monthly_real_return, n_months) - 1) /                                    (monthly_real_return * math.pow(1 + monthly_real_return, n_months))
        recommended_contribution = recommended_contribution / 12  # Mensuel
    else:
        recommended_contribution = monthly_contribution

    return RetirementSimulationResult(
        years_to_retirement=years_to_retirement,
        total_accumulated=round(total_accumulated, 2),
        monthly_pension=round(monthly_pension, 2),
        pension_gap=round(max(pension_gap, 0), 2),
        replacement_rate=round(replacement_rate, 2),
        is_on_track=is_on_track,
        recommended_contribution=round(recommended_contribution, 2),
        yearly_breakdown=yearly_breakdown
    )

# ==================== ANALYSE BUDGET ====================
def analyze_budget(budget_data: Dict[str, Any]) -> BudgetAnalysis:
    """
    Analyse un budget et fournit des recommandations
    """
    total_income = budget_data.get("monthly_income", 0) + budget_data.get("additional_income", 0)

    expenses = {
        "Logement": budget_data.get("housing_expense", 0),
        "Transport": budget_data.get("transport_expense", 0),
        "Alimentation": budget_data.get("food_expense", 0),
        "Santé": budget_data.get("health_expense", 0),
        "Éducation": budget_data.get("education_expense", 0),
        "Loisirs": budget_data.get("leisure_expense", 0),
        "Épargne": budget_data.get("savings_goal", 0),
        "Autres": budget_data.get("other_expenses", 0)
    }

    total_expenses = sum(expenses.values())
    remaining = total_income - total_expenses
    savings_rate = (budget_data.get("savings_goal", 0) / total_income * 100) if total_income > 0 else 0

    # Répartition des dépenses
    expense_breakdown = []
    for category, amount in expenses.items():
        if amount > 0:
            expense_breakdown.append({
                "category": category,
                "amount": amount,
                "percent": round((amount / total_income * 100), 1) if total_income > 0 else 0
            })

    # Recommandations
    recommendations = []

    # Règle 50/30/20
    needs = expenses["Logement"] + expenses["Transport"] + expenses["Alimentation"] + expenses["Santé"]
    wants = expenses["Loisirs"] + expenses["Éducation"] + expenses["Autres"]

    needs_percent = (needs / total_income * 100) if total_income > 0 else 0
    wants_percent = (wants / total_income * 100) if total_income > 0 else 0

    if needs_percent > 50:
        recommendations.append(f"Vos besoins essentiels représentent {needs_percent:.0f}% de vos revenus (recommandé : 50%). Envisagez de réduire vos dépenses de logement ou transport.")

    if wants_percent > 30:
        recommendations.append(f"Vos dépenses discrétionnaires représentent {wants_percent:.0f}% de vos revenus (recommandé : 30%). Opportunité d'économiser {round(wants - total_income * 0.3, 0)} DH/mois.")

    if savings_rate < 20:
        recommendations.append(f"Votre taux d'épargne est de {savings_rate:.0f}% (recommandé : 20%). Augmentez votre épargne de {round(total_income * 0.2 - budget_data.get('savings_goal', 0), 0)} DH/mois pour atteindre 20%.")

    if remaining < 0:
        recommendations.append(f"⚠️ Vous êtes en déficit de {abs(remaining):.0f} DH/mois ! Réduisez immédiatement vos dépenses ou augmentez vos revenus.")

    # Potentiel d'épargne par catégorie
    savings_potential = []

    # Alimentation
    food_expense = expenses["Alimentation"]
    if food_expense > total_income * 0.15:
        potential = food_expense - total_income * 0.15
        savings_potential.append({
            "category": "Alimentation",
            "current": food_expense,
            "recommended": round(total_income * 0.15, 0),
            "potential": round(potential, 0),
            "tips": ["Faire les courses avec une liste", "Cuisiner à la maison", "Éviter le gaspillage alimentaire"]
        })

    # Transport
    transport_expense = expenses["Transport"]
    if transport_expense > total_income * 0.10:
        potential = transport_expense - total_income * 0.10
        savings_potential.append({
            "category": "Transport",
            "current": transport_expense,
            "recommended": round(total_income * 0.10, 0),
            "potential": round(potential, 0),
            "tips": ["Utiliser les transports en commun", "Covoiturage", "Vélo pour les courts trajets"]
        })

    # Loisirs
    leisure_expense = expenses["Loisirs"]
    if leisure_expense > total_income * 0.10:
        potential = leisure_expense - total_income * 0.10
        savings_potential.append({
            "category": "Loisirs",
            "current": leisure_expense,
            "recommended": round(total_income * 0.10, 0),
            "potential": round(potential, 0),
            "tips": ["Profiter des activités gratuites", "Cartes de réduction", "Planifier les sorties à l'avance"]
        })

    # Logement
    housing_expense = expenses["Logement"]
    if housing_expense > total_income * 0.30:
        potential = housing_expense - total_income * 0.30
        savings_potential.append({
            "category": "Logement",
            "current": housing_expense,
            "recommended": round(total_income * 0.30, 0),
            "potential": round(potential, 0),
            "tips": ["Négocier le loyer", "Chercher un colocataire", "Déménager dans une zone moins chère"]
        })

    return BudgetAnalysis(
        total_income=round(total_income, 2),
        total_expenses=round(total_expenses, 2),
        remaining=round(remaining, 2),
        savings_rate=round(savings_rate, 2),
        expense_breakdown=expense_breakdown,
        recommendations=recommendations,
        savings_potential=savings_potential
    )
