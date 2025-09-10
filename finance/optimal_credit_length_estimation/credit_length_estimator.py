import sys
from detail.input import parse_input, validate_input, write_test_input
from detail.investment import calculate_simple_investment
from credit.simple_credit import calculate_credit
from detail.visualization import plot_credit_results
from credit.credit_with_investment import calculate_credit_with_investment

def print_credit_parameters(credit_parameters):
    for key in credit_parameters:
        print(f"{key}: {credit_parameters.get(key)}")


def main():
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

    credit_results = calculate_credit(credit_parameters)
    print("\nCredit calculations:")
    for years, data in credit_results.items():
        print(
            f"{years} years: Monthly payment: {data['monthly_payment']}, Total cost: {data['total_cost']}, Inflation-adjusted cost: {data['total_cost_adjusted']}"
        )
        if (
            credit_parameters["Acceptable monthly payment"][0]
            >= data["monthly_payment"]
        ):
            investment_account_balance = calculate_simple_investment(
                0,
                credit_parameters["Acceptable monthly payment"][0] - data["monthly_payment"],
                credit_parameters["Investment interest rate"][0],
                years,
            )
            print(
                f"  Investment account balance after {years} years: {investment_account_balance}"
            )

    # Calculate credit with investment
    investment_results = calculate_credit_with_investment(
        credit_results, credit_parameters
    )

    print("\nCredit with investment calculations:")
    for years, data in investment_results.items():
        print(
            f"{years} years: Monthly payment: {data['monthly_payment']}, Total cost: {data['total_cost']}, Inflation-adjusted cost: {data['total_cost_adjusted']}"
        )

    plot_credit_results(
        credit_results,
        credit_parameters["Acceptable monthly payment"][0],
        investment_results,
    )


if __name__ == "__main__":
    main()
