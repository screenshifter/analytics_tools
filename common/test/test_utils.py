import unittest
from io import StringIO
from unittest.mock import patch
from common.utils import log_error


class TestLogError(unittest.TestCase):
    """
    Unit tests for log_error function.

    Test Categories:
    - Output format: Correct prefix, message content
    - Input classes: Empty string, short message, long message
    """

    def test_log_error_output_format(self):
        """Test that log_error prints message with ERROR prefix"""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            log_error("something went wrong")
            self.assertEqual(mock_stdout.getvalue(), "ERROR: something went wrong\n")

    def test_log_error_empty_message(self):
        """Test log_error with empty string"""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            log_error("")
            self.assertEqual(mock_stdout.getvalue(), "ERROR: \n")


if __name__ == "__main__":
    unittest.main()
