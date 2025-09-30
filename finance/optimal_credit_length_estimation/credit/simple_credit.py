from typing import Dict, Any


def _calculate_monthly_payment(amount: float, rate: float, months: int) -> float:
    """Calculate monthly payment for given loan parameters"""
    if rate == 0:
        return amount / months

    rate_factor = (1 + rate) ** months
    numerator = rate * rate_factor
    denominator = rate_factor - 1
    return amount * (numerator / denominator)


def calculate_credit(credit_parameters: Dict[str, Any]) -> Dict[int, Dict[str, float]]:
    """Calculates credit payments for different loan terms. Additionally calculates total credit cost adjusted to inflation in "today's" money

    Args:
        credit_parameters (dict): Contains "Credit amount", "Credit rate", "Expected inflation"

    Returns:
        dict: Results for each year (3-30) with monthly payment and total cost
    """
    amount = credit_parameters["Credit amount"]
    rate = (
        credit_parameters["Credit rate"][0] / 100 / 12
    )  # Convert to monthly decimal rate
    inflation_rate = (
        credit_parameters["Expected inflation"][0] / 100
    )  # Annual inflation rate

    results = {}
    for years in range(3, 31):
        months = years * 12

        # Calculate monthly payment
        monthly_payment = _calculate_monthly_payment(amount, rate, months)

        total_cost = monthly_payment * months

        # Calculate inflation-adjusted total cost
        inflation_factor = (1 + inflation_rate) ** years
        total_cost_adjusted = total_cost / inflation_factor

        results[years] = {
            "monthly_payment": round(monthly_payment, 2),
            "total_cost": round(total_cost, 2),
            "total_cost_adjusted": round(total_cost_adjusted, 2),
            "investment_balance": 0,
        }

    return results


def calculate_credit_with_overpayment(credit_parameters: Dict[str, Any]) -> Dict[int, Dict[str, float]]:
    """Calculates credit with overpayment when monthly payment is below acceptable threshold
    
    Args:
        credit_parameters (dict): Contains "Credit amount", "Credit rate", "Expected inflation", "Acceptable monthly payment"
        
    Returns:
        dict: Results for each year (3-30) with actual payment time and costs
    """
    amount = credit_parameters["Credit amount"]
    rate = credit_parameters["Credit rate"][0] / 100 / 12
    inflation_rate = credit_parameters["Expected inflation"][0] / 100
    acceptable_payment = credit_parameters["Acceptable monthly payment"][0]
    
    results = {}
    for years in range(3, 31):
        months = years * 12
        
        # Calculate standard monthly payment
        standard_payment = _calculate_monthly_payment(amount, rate, months)
        
        if standard_payment >= acceptable_payment:
            # No overpayment possible
            total_cost = standard_payment * months
            inflation_factor = (1 + inflation_rate) ** years
            total_cost_adjusted = total_cost / inflation_factor
            
            results[years] = {
                "monthly_payment": round(standard_payment, 2),
                "total_cost": round(total_cost, 2),
                "total_cost_adjusted": round(total_cost_adjusted, 2),
                "investment_balance": 0,
                "actual_months": months
            }
        else:
            # Calculate with overpayment
            overpayment = acceptable_payment - standard_payment
            actual_payment = acceptable_payment
            
            # Calculate actual payoff time with overpayment
            remaining_balance = amount
            actual_months = 0
            total_paid = 0
            
            while remaining_balance > 0.01 and actual_months < months:
                interest_payment = remaining_balance * rate
                principal_payment = actual_payment - interest_payment
                
                if principal_payment <= 0:
                    break
                    
                remaining_balance -= principal_payment
                total_paid += actual_payment
                actual_months += 1
            
            actual_years = actual_months / 12
            inflation_factor = (1 + inflation_rate) ** actual_years
            total_cost_adjusted = total_paid / inflation_factor
            
            results[years] = {
                "monthly_payment": round(actual_payment, 2),
                "total_cost": round(total_paid, 2),
                "total_cost_adjusted": round(total_cost_adjusted, 2),
                "investment_balance": 0,
                "actual_months": actual_months
            }
    
    return results
