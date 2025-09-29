import matplotlib.pyplot as plt


def plot_credit_results(credit_results, acceptable_monthly_payment=None, investment_results=None):
    """Creates individual plots for each credit result metric over years"""
    years = list(credit_results.keys())
    monthly_payments = [data["monthly_payment"] for data in credit_results.values()]
    total_costs = [data["total_cost"] for data in credit_results.values()]
    total_costs_adjusted = [
        data["total_cost_adjusted"] for data in credit_results.values()
    ]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    ax1.plot(years, monthly_payments, "b-", marker="o", label="Credit Only")
    if acceptable_monthly_payment:
        ax1.axhline(
            y=acceptable_monthly_payment,
            color="r",
            linestyle="--",
            label="Acceptable Payment",
        )
    if investment_results:
        inv_monthly_payments = [data["monthly_payment"] for data in investment_results.values()]
        ax1.plot(years, inv_monthly_payments, "orange", marker="o", label="With Investment")
    ax1.legend()
    ax1.set_title("Monthly Payment vs Years")
    ax1.set_xlabel("Years")
    ax1.set_ylabel("Monthly Payment")
    ax1.grid(True)

    ax2.plot(years, total_costs, "r-", marker="s", label="Credit Only")
    if investment_results:
        inv_total_costs = [data["total_cost"] for data in investment_results.values()]
        ax2.plot(years, inv_total_costs, "purple", marker="s", label="With Investment")
    ax2.legend()
    ax2.set_title("Total Cost vs Years")
    ax2.set_xlabel("Years")
    ax2.set_ylabel("Total Cost")
    ax2.grid(True)

    ax3.plot(years, total_costs_adjusted, "g-", marker="^", label="Credit Only")
    if investment_results:
        inv_total_costs_adjusted = [data["total_cost_adjusted"] for data in investment_results.values()]
        ax3.plot(years, inv_total_costs_adjusted, "brown", marker="^", label="With Investment")
    ax3.legend()
    ax3.set_title("Inflation-Adjusted Cost vs Years")
    ax3.set_xlabel("Years")
    ax3.set_ylabel("Inflation-Adjusted Cost")
    ax3.grid(True)

    plt.tight_layout()
    plt.show()
