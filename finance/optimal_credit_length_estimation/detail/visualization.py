import matplotlib.pyplot as plt
from typing import List, Dict, Any


def plot_credit_results(results_list: List[Dict[str, Any]], credit_parameters: Dict[str, Any]) -> None:
    """Creates individual plots for each credit result metric over years"""
    if not results_list:
        return
    
    years = list(results_list[0]["results"].keys())
    colors = ["b", "orange", "green", "purple", "cyan"]
    markers = ["o", "s", "^", "d", "v"]
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot monthly payments
    for i, result_set in enumerate(results_list):
        monthly_payments = [data["monthly_payment"] for data in result_set["results"].values()]
        ax1.plot(years, monthly_payments, color=colors[i % len(colors)], marker=markers[i % len(markers)], label=result_set["label"])
    
    # Add acceptable payment line
    if "Acceptable monthly payment" in credit_parameters:
        ax1.axhline(
            y=credit_parameters["Acceptable monthly payment"][0],
            color="r",
            linestyle="--",
            label="Acceptable Payment",
        )
    
    ax1.legend()
    ax1.set_title("Monthly Payment vs Years")
    ax1.set_xlabel("Years")
    ax1.set_ylabel("Monthly Payment")
    ax1.grid(True)
    
    # Plot total costs
    for i, result_set in enumerate(results_list):
        total_costs = [data["total_cost"] for data in result_set["results"].values()]
        ax2.plot(years, total_costs, color=colors[i % len(colors)], marker=markers[i % len(markers)], label=result_set["label"])
    
    ax2.legend()
    ax2.set_title("Total Cost vs Years")
    ax2.set_xlabel("Years")
    ax2.set_ylabel("Total Cost")
    ax2.grid(True)
    
    # Plot inflation-adjusted costs
    for i, result_set in enumerate(results_list):
        total_costs_adjusted = [data["total_cost_adjusted"] for data in result_set["results"].values()]
        ax3.plot(years, total_costs_adjusted, color=colors[i % len(colors)], marker=markers[i % len(markers)], label=result_set["label"])
    
    ax3.legend()
    ax3.set_title("Inflation-Adjusted Cost vs Years")
    ax3.set_xlabel("Years")
    ax3.set_ylabel("Inflation-Adjusted Cost")
    ax3.grid(True)
    
    plt.tight_layout()
    plt.show()
