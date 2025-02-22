import sys
from detail.input import parse_input, validate_input, write_test_input
from detail.simple_credit import calculate_credit
from detail.visualization import plot_credit_results


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

    if not write_test_input(filepath):
        sys.exit("Unable to write test file")

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

    plot_credit_results(credit_results)


if __name__ == "__main__":
    main()
