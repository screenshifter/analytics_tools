from detail.investment import calculate_simple_investment


def calculate_credit_with_investment(credit_results, credit_parameters):
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
    
    results = {}
    
    for years, data in credit_results.items():
        actual_monthly_payment = max(acceptable_monthly_payment, data['monthly_payment'])
        monthly_investment = max(0, acceptable_monthly_payment - data['monthly_payment'])
        
        investment_balance = calculate_simple_investment(
            0, monthly_investment, investment_rate, years
        )
        
        total_cost_with_investment = data['total_cost'] - investment_balance
        
        # Calculate inflation-adjusted total cost
        inflation_factor = (1 + inflation_rate / 100) ** years
        total_cost_adjusted_with_investment = total_cost_with_investment / inflation_factor
        
        results[years] = {
            'monthly_payment': actual_monthly_payment,
            'total_cost': total_cost_with_investment,
            'total_cost_adjusted': round(total_cost_adjusted_with_investment, 2),
            'investment_balance': round(investment_balance, 2)
        }
    
    return results