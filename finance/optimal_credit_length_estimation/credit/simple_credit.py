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


def _calculate_payoff_with_overpayment(
    amount: float, rate: float, payment: float, max_months: int
) -> tuple[int, float]:
    """Calculate actual payoff time and total paid with overpayment"""
    remaining_balance = amount
    actual_months = 0
    total_paid = 0

    while remaining_balance > 0.01 and actual_months < max_months:
        interest_payment = remaining_balance * rate
        principal_payment = payment - interest_payment

        if principal_payment <= 0:
            break

        remaining_balance -= principal_payment
        total_paid += payment
        actual_months += 1

    return actual_months, total_paid


def _apply_inflation_adjustment(
    cost: float, inflation_rate: float, years: int
) -> float:
    """Apply inflation adjustment to cost"""
    inflation_factor = (1 + inflation_rate) ** years
    return cost / inflation_factor


def _calculate_investment_balance(
    monthly_payment: float, investment_rate: float, remaining_months: int
) -> float:
    """Calculate investment balance for remaining months after payoff"""
    if remaining_months <= 0:
        return 0

    from detail.investment import calculate_simple_investment

    return calculate_simple_investment(
        0, monthly_payment, investment_rate, remaining_months / 12
    )


def calculate_credit(
    credit_parameters: dict[str, Any],
) -> dict[int, CreditCalculationResult]:
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
        total_cost_adjusted = _apply_inflation_adjustment(
            total_cost, inflation_rate, years
        )

        results[years] = CreditCalculationResult(
            monthly_payment=round(monthly_payment, 2),
            total_cost=round(total_cost, 2),
            total_cost_adjusted=round(total_cost_adjusted, 2),
            investment_balance=0,
        )

    return results


def calculate_credit_with_overpayment(
    credit_parameters: dict[str, Any],
) -> dict[int, CreditCalculationResult]:
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
            monthly_payment = standard_payment
            total_cost = standard_payment * months
            investment_balance = 0
        else:
            # Calculate with overpayment
            monthly_payment = acceptable_payment

            # Calculate actual payoff time with overpayment
            actual_months, total_paid = _calculate_payoff_with_overpayment(
                amount, rate, monthly_payment, months
            )

            # Calculate investment balance for remaining months after payoff
            remaining_months = months - actual_months
            investment_rate = credit_parameters["Investment interest rate"][0]
            investment_balance = _calculate_investment_balance(
                monthly_payment, investment_rate, remaining_months
            )

            # Calculate total cost with investment balance subtracted
            total_cost = total_paid - investment_balance

        # Calculate inflation-adjusted total cost
        total_cost_adjusted = _apply_inflation_adjustment(
            total_cost, inflation_rate, years
        )

        results[years] = CreditCalculationResult(
            monthly_payment=round(monthly_payment, 2),
            total_cost=round(total_cost, 2),
            total_cost_adjusted=round(total_cost_adjusted, 2),
            investment_balance=round(investment_balance, 2),
        )

    return results


def calculate_credit_with_investment(
    credit_results: dict[int, CreditCalculationResult],
    credit_parameters: dict[str, Any],
) -> dict[int, CreditCalculationResult]:
    """Calculate credit results with investment of payment difference

    Args:
        credit_results (dict): Results from calculate_credit function
        credit_parameters (dict): Credit parameters containing acceptable payment, investment rate, and inflation

    Returns:
        dict: Modified results with investment calculations
    """
    acceptable_monthly_payment = credit_parameters["Acceptable monthly payment"][0]
    investment_rate = credit_parameters["Investment interest rate"][0]
    inflation_rate = credit_parameters["Expected inflation"][0]

    results: dict[int, CreditCalculationResult] = {}

    for years, data in credit_results.items():
        actual_monthly_payment = max(
            acceptable_monthly_payment, data["monthly_payment"]
        )
        monthly_investment = max(
            0, acceptable_monthly_payment - data["monthly_payment"]
        )

        from detail.investment import calculate_simple_investment

        investment_balance = calculate_simple_investment(
            0, monthly_investment, investment_rate, years
        )

        total_cost_with_investment = data["total_cost"] - investment_balance

        # Calculate inflation-adjusted total cost
        inflation_factor = (1 + inflation_rate / 100) ** years
        total_cost_adjusted_with_investment = (
            total_cost_with_investment / inflation_factor
        )

        results[years] = CreditCalculationResult(
            monthly_payment=actual_monthly_payment,
            total_cost=total_cost_with_investment,
            total_cost_adjusted=round(total_cost_adjusted_with_investment, 2),
            investment_balance=round(investment_balance, 2),
        )

    return results
