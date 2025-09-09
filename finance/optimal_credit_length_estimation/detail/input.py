import json
import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from common.utils import log_error


def parse_input(filepath):
    """Parses input file

    Returns:
        A Python library representation of the input parameters or 'False' if an error occured
    """
    # Sanitize filepath to prevent path traversal
    filepath = os.path.normpath(filepath)
    if ".." in filepath:
        log_error("Path traversal detected")
        return False

    with open(filepath) as input_file:
        try:
            input_conditions = json.load(input_file)
        except ValueError as failure:
            log_error(f"An error occured during input file decoding: {failure.args}")
            return False
        return input_conditions


def validate_input(sample):
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
        if key not in sample:
            log_error(
                f"There's no {key} in the input file, please set a value under the '{key}' key"
            )
            return False

    keys_with_multiple_values = [
        "Credit rate",
        "Expected inflation",
    ]
    for key in keys_with_multiple_values:
        if not sample.get(key):
            log_error(f"{key} is empty, please add some values under the '{key}' key")
            return False

    return True


def write_test_input(filepath):
    """Generates test input data and writes it to the input file"""
    data_to_write = {
        "Credit amount": 600000,
        "Credit rate": [8.0],
        "Expected inflation": [3.0],
        "Acceptable monthly payment": [6000],
        "Investment interest rate": [5.0],
    }
    try:
        with open(
            filepath,
            mode="w",
        ) as input_file:
            json.dump(obj=data_to_write, fp=input_file)
    except (IOError, OSError) as e:
        log_error(f"Failed to write test input file: {e}")
        return False
    return True
