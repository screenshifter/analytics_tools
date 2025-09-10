def calculate_simple_investment(
    initial_investment, monthly_income, interest_rate, years
):
    """Calculate total balance for investment with regular monthly contributions

    Args:
        initial_investment (float): Initial lump sum investment
        monthly_income (float): Monthly contribution amount
        interest_rate (float): Annual interest rate as percentage (e.g., 5.0 for 5%)
        years (int): Investment period in years

    Returns:
        float: Total balance after the investment period
    """
    if initial_investment < 0:
        raise ValueError("Initial investment cannot be negative")
    if monthly_income < 0:
        raise ValueError("Monthly income cannot be negative")
    if interest_rate < 0:
        raise ValueError("Interest rate cannot be negative")
    if years <= 0:
        raise ValueError("Years must be positive")
    
    monthly_rate = interest_rate / 100 / 12
    months = years * 12

    # Calculate future value of initial investment
    initial_future_value = initial_investment * ((1 + monthly_rate) ** months)

    # Calculate future value of monthly contributions (annuity)
    if monthly_rate == 0:
        annuity_future_value = monthly_income * months
    else:
        annuity_future_value = monthly_income * (
            ((1 + monthly_rate) ** months - 1) / monthly_rate
        )

    return round(initial_future_value + annuity_future_value, 2)
