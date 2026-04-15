import matplotlib.figure
import sys
import os.path
from python.runfiles import runfiles
# Use paths relative to the project root to allow to use the script both directly and with Bazel
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from typing import Any
from finance.optimal_credit_length_estimation.input.input import parse_input, validate_input
from finance.optimal_credit_length_estimation.detail.types import CreditCalculationResult
from finance.optimal_credit_length_estimation.credit.simple_credit import (
    calculate_credit,
    calculate_credit_with_overpayment,
    calculate_credit_with_investment,
)
from finance.optimal_credit_length_estimation.user_interface.visualization import plot_credit_results


def print_credit_parameters(credit_parameters: dict[str, Any]) -> None:
    for key in credit_parameters:
        print(f"{key}: {credit_parameters.get(key)}")


def print_credit_results(
    results: dict[int, CreditCalculationResult], calculation_name: str
) -> None:
    """Print credit calculation results in a standardized format"""
    print(f"\n{calculation_name}:")
    for years, data in results.items():
        investment_balance = data.get("investment_balance", 0)
        print(
            f"{years} years: Monthly payment: {data['monthly_payment']}, Total cost: {data['total_cost']}, Inflation-adjusted cost: {data['total_cost_adjusted']}, Investment balance: {investment_balance}"
        )


def get_credit_figure() -> matplotlib.figure.Figure:
    filepath = runfiles.Create().Rlocation(
        "analytics_tools/finance/optimal_credit_length_estimation/input/default_input.json"
    )
    credit_parameters = parse_input(filepath)
    if not credit_parameters or not validate_input(credit_parameters):
        raise RuntimeError("Failed to load or validate credit input")

    all_results: list[dict[str, Any]] = [
        {"results": calculate_credit(credit_parameters), "label": "Credit Only"},
        {"results": calculate_credit_with_investment(credit_parameters), "label": "With Investment"},
        {"results": calculate_credit_with_overpayment(credit_parameters), "label": "With Overpayment"},
    ]
    return plot_credit_results(all_results, credit_parameters)


def main() -> None:
    filepath = (
        sys.argv[1]
        if len(sys.argv) > 1
        else runfiles.Create().Rlocation(
            "analytics_tools/finance/optimal_credit_length_estimation/input/default_input.json"
        )
    )
    print(f"Credit parameters input file path: {filepath}")

    credit_parameters = parse_input(filepath)
    if not credit_parameters:
        sys.exit("Unrecoverable error, exiting")
    if not validate_input(credit_parameters):
        sys.exit("Provided data has incorrect format, can't proceed")

    print_credit_parameters(credit_parameters)

    # Calculate credits
    credit_results = calculate_credit(credit_parameters)
    investment_results = calculate_credit_with_investment(credit_parameters)
    overpayment_results = calculate_credit_with_overpayment(credit_parameters)

    # Print and visualize the results
    print_credit_results(credit_results, "Credit calculations")
    print_credit_results(investment_results, "Credit with investment calculations")
    print_credit_results(overpayment_results, "Credit with overpayment calculations")

    all_results: list[dict[str, Any]] = [
        {"results": credit_results, "label": "Credit Only"},
        {"results": investment_results, "label": "With Investment"},
        {"results": overpayment_results, "label": "With Overpayment"},
    ]
    fig = plot_credit_results(all_results, credit_parameters)
    fig.show()


if __name__ == "__main__":
    main()
