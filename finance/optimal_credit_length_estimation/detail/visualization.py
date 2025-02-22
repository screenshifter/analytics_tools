import matplotlib.pyplot as plt


def plot_credit_results(credit_results):
    """Creates individual plots for each credit result metric over years"""
    years = list(credit_results.keys())
    monthly_payments = [data["monthly_payment"] for data in credit_results.values()]
    total_costs = [data["total_cost"] for data in credit_results.values()]
    total_costs_adjusted = [
        data["total_cost_adjusted"] for data in credit_results.values()
    ]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    ax1.plot(years, monthly_payments, "b-", marker="o")
    ax1.set_title("Monthly Payment vs Years")
    ax1.set_xlabel("Years")
    ax1.set_ylabel("Monthly Payment")
    ax1.grid(True)

    ax2.plot(years, total_costs, "r-", marker="s")
    ax2.set_title("Total Cost vs Years")
    ax2.set_xlabel("Years")
    ax2.set_ylabel("Total Cost")
    ax2.grid(True)

    ax3.plot(years, total_costs_adjusted, "g-", marker="^")
    ax3.set_title("Inflation-Adjusted Cost vs Years")
    ax3.set_xlabel("Years")
    ax3.set_ylabel("Inflation-Adjusted Cost")
    ax3.grid(True)

    plt.tight_layout()
    plt.show()
