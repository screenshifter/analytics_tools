from typing import Any
from detail.types import CreditCalculationResult


def _calculate_monthly_payment(amount: float, rate: float, months: int) -> float:
    """Calculate monthly payment for given loan parameters"""
    if rate == 0:
        return amount / months

    rate_factor = (1 + rate) ** months
    numerator = rate * rate_factor
    denominator = rate_factor - 1
    return amount * (numerator / denominator)


def calculate_credit(credit_parameters: dict[str, Any]) -> dict[int, CreditCalculationResult]:
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

    results: dict[int, CreditCalculationResult] = {}
    for years in range(3, 31):
        months = years * 12

        # Calculate monthly payment
        monthly_payment = _calculate_monthly_payment(amount, rate, months)

        total_cost = monthly_payment * months

        # Calculate inflation-adjusted total cost
        inflation_factor = (1 + inflation_rate) ** years
        total_cost_adjusted = total_cost / inflation_factor

        results[years] = CreditCalculationResult(
            monthly_payment=round(monthly_payment, 2),
            total_cost=round(total_cost, 2),
            total_cost_adjusted=round(total_cost_adjusted, 2),
            investment_balance=0,
        )

    return results


def calculate_credit_with_overpayment(credit_parameters: dict[str, Any]) -> dict[int, CreditCalculationResult]:
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
    
    results: dict[int, CreditCalculationResult] = {}
    for years in range(3, 31):
        months = years * 12
        
        # Calculate standard monthly payment
        standard_payment = _calculate_monthly_payment(amount, rate, months)
        
        if standard_payment >= acceptable_payment:
            # No overpayment possible
            total_cost = standard_payment * months
            inflation_factor = (1 + inflation_rate) ** years
            total_cost_adjusted = total_cost / inflation_factor
            
            results[years] = CreditCalculationResult(
                monthly_payment=round(standard_payment, 2),
                total_cost=round(total_cost, 2),
                total_cost_adjusted=round(total_cost_adjusted, 2),
                investment_balance=0,
            )
        else:
            # Calculate with overpayment
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
            
            # Calculate investment balance for remaining months after payoff
            remaining_months = months - actual_months
            if remaining_months > 0:
                from detail.investment import calculate_simple_investment
                investment_rate = credit_parameters["Investment interest rate"][0]
                investment_balance = calculate_simple_investment(
                    0,
                    acceptable_payment,
                    investment_rate,
                    remaining_months / 12
                )
            else:
                investment_balance = 0
            
            # Calculate total cost with investment balance subtracted
            total_cost_with_investment = total_paid - investment_balance
            
            # Calculate inflation-adjusted total cost using the new total cost and full loan term
            inflation_factor = (1 + inflation_rate) ** years
            total_cost_adjusted = total_cost_with_investment / inflation_factor
            
            results[years] = CreditCalculationResult(
                monthly_payment=round(actual_payment, 2),
                total_cost=round(total_cost_with_investment, 2),
                total_cost_adjusted=round(total_cost_adjusted, 2),
                investment_balance=round(investment_balance, 2),
            )
    
    return results
