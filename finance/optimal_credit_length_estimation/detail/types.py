from typing import TypedDict


class CreditCalculationResult(TypedDict):
    monthly_payment: float
    total_cost: float
    total_cost_adjusted: float
    investment_balance: float
