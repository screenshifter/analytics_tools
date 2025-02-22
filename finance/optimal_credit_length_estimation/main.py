import json
import sys


def LogError(message):
    print(f"ERROR: {message}")


def ParseInput():
    """Parses input file

    Returns:
        A Python library representation of the input parameters or 'False' if an error occured
    """
    with open("./input/input.json") as input_file:
        try:
            input_conditions = json.load(input_file)
        except ValueError as failure:
            LogError(f"An error occured during input file decoding: {failure.args}")
            return False
        return input_conditions


def ValidateInput(sample):
    """Validates input data

    Data is checked to have all required parameters and some values for them

    Args:
        sample (dict): Python representation of the input JSON file

    Returns:
        bool: True if the validation have passed, False otherwise
    """

    keys = [
        "Credit amount",
        "Credit rate",
        "Expected inflation",
    ]
    for key in keys:
        try:
            sample[key]
        except KeyError:
            LogError(
                f"There's no {key} in the input file, please set a value under the '{key}' key"
            )
            return False

    keys_with_multiple_values = [
        "Credit rate",
        "Expected inflation",
    ]
    for key in keys_with_multiple_values:
        if len(sample.get(key)) == 0:
            LogError(f"{key} is empty, please add some values under the '{key}' key")
            return False

    return True


def PrintInputData(input_data):
    for key in input_data:
        print(f"{key}: {input_data.get(key)}")


## TODO: Development phase function, please remove after completing the development
def WriteTestInput():
    """Generates test input data and writes it to the input file"""
    data_to_write = {
        "Credit amount": 600000,
        "Credit rate": [8.0, 7.0],
        "Expected inflation": [3.0, 4.0, 2.0],
    }
    # TODO: fix this to use environment variable correctly
    # the idea is to just clone the whole repo and set up the minimal number of infrastructure to have it functional
    # TODO: add this to the global README.md
    with open(
        file="$ANALYTICS_TOOLS/finance/optimal_credit_length_estimation/input/input.json",
        mode="w",
    ) as input_file:
        json.dump(obj=data_to_write, fp=input_file)


## main body
WriteTestInput()

input_data = ParseInput()
if not input_data:
    sys.exit("Unrecoverable error, exiting")
if not ValidateInput(input_data):
    sys.exit("Provided data has incorrect format, can't proceed")

PrintInputData(input_data)
