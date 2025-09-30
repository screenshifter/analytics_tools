import json
import os.path
import sys
from typing import Dict, Any

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from common.utils import log_error


def parse_input(filepath: str) -> Dict[str, Any]:
    """Parses input file

    Returns:
        A Python library representation of the input parameters or 'False' if an error occured
    """
    # Sanitize filepath
    filepath = os.path.abspath(os.path.normpath(filepath))
    if not os.path.exists(filepath):
        log_error(f"File not found: {filepath}")
        return dict()

    with open(filepath) as input_file:
        try:
            input_conditions = json.load(input_file)
        except ValueError as failure:
            log_error(f"An error occured during input file decoding: {failure.args}")
            return dict()
        return input_conditions


def validate_input(sample: Dict[str, Any]) -> bool:
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
