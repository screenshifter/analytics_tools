def _calculate_monthly_payment(amount, rate, months):
    """Calculate monthly payment for given loan parameters"""
    if rate == 0:
        return amount / months

    rate_factor = (1 + rate) ** months
    numerator = rate * rate_factor
    denominator = rate_factor - 1
    return amount * (numerator / denominator)


def calculate_credit(credit_parameters):
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
        }

    return results
