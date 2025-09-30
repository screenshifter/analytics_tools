import sys
from typing import Dict, Any
from detail.input import parse_input, validate_input, write_test_input
from credit.simple_credit import calculate_credit, calculate_credit_with_overpayment
from detail.visualization import plot_credit_results
from credit.credit_with_investment import calculate_credit_with_investment


def print_credit_parameters(credit_parameters: Dict[str, Any]) -> None:
    for key in credit_parameters:
        print(f"{key}: {credit_parameters.get(key)}")


def print_credit_results(results: Dict[int, Dict[str, float]], calculation_name: str) -> None:
    """Print credit calculation results in a standardized format"""
    print(f"\n{calculation_name}:")
    for years, data in results.items():
        investment_balance = data.get("investment_balance", 0)
        print(
            f"{years} years: Monthly payment: {data['monthly_payment']}, Total cost: {data['total_cost']}, Inflation-adjusted cost: {data['total_cost_adjusted']}, Investment balance: {investment_balance}"
        )


def main() -> None:
    filepath = (
        sys.argv[1]
        if len(sys.argv) > 1
        else (sys.path[0] + "/input/default_input.json")
    )
    print(f"Credit parameters input file path: {filepath}")

    # if not write_test_input(filepath):
    #     sys.exit("Unable to write test file")

    credit_parameters = parse_input(filepath)
    if not credit_parameters:
        sys.exit("Unrecoverable error, exiting")
    if not validate_input(credit_parameters):
        sys.exit("Provided data has incorrect format, can't proceed")

    print_credit_parameters(credit_parameters)

    # Calculate credits
    credit_results = calculate_credit(credit_parameters)
    investment_results = calculate_credit_with_investment(
        credit_results, credit_parameters
    )
    overpayment_results = calculate_credit_with_overpayment(credit_parameters)

    # Print and visualize the results
    print_credit_results(credit_results, "Credit calculations")
    print_credit_results(investment_results, "Credit with investment calculations")
    print_credit_results(overpayment_results, "Credit with overpayment calculations")

    all_results = [
        {"results": credit_results, "label": "Credit Only"},
        {"results": investment_results, "label": "With Investment"},
        {"results": overpayment_results, "label": "With Overpayment"},
    ]
    plot_credit_results(all_results, credit_parameters)


if __name__ == "__main__":
    main()
