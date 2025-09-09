import unittest
import math
from ..simple_credit import calculate_credit


class TestSimpleCreditCalculation(unittest.TestCase):

    def test_basic_calculation(self):
        """Test basic credit calculation with known values"""
        credit_params = {
            "Credit amount": 100000,
            "Credit rate": [6.0],
            "Expected inflation": [0.0],
        }
        results = calculate_credit(credit_params)

        # Test 10-year loan
        result_10y = results[10]
        expected_monthly = 1110.21  # Known value for 6% APR, 10 years, 100k
        self.assertAlmostEqual(
            result_10y["monthly_payment"], expected_monthly, places=0
        )

    def test_zero_interest_rate(self):
        """Test calculation with zero interest rate"""
        credit_params = {
            "Credit amount": 120000,
            "Credit rate": [0.0],
            "Expected inflation": [0.0],
        }
        results = calculate_credit(credit_params)

        # With 0% interest, monthly payment should be amount / months
        result_10y = results[10]
        expected_monthly = 120000 / (10 * 12)  # 1000
        self.assertEqual(result_10y["monthly_payment"], expected_monthly)
        self.assertEqual(result_10y["total_cost"], 120000)

    def test_inflation_adjustment(self):
        """Test inflation adjustment calculation"""
        credit_params = {
            "Credit amount": 100000,
            "Credit rate": [0.0],
            "Expected inflation": [3.0],
        }
        results = calculate_credit(credit_params)

        result_10y = results[10]
        # With 3% inflation over 10 years, adjusted cost should be lower
        inflation_factor = (1 + 0.03) ** 10
        expected_adjusted = result_10y["total_cost"] / inflation_factor
        self.assertAlmostEqual(
            result_10y["total_cost_adjusted"], expected_adjusted, places=2
        )

    def test_all_years_present(self):
        """Test that results include all years from 3 to 30"""
        credit_params = {
            "Credit amount": 50000,
            "Credit rate": [5.0],
            "Expected inflation": [2.0],
        }
        results = calculate_credit(credit_params)

        expected_years = list(range(3, 31))
        self.assertEqual(list(results.keys()), expected_years)

    def test_longer_term_lower_payment(self):
        """Test that longer terms result in lower monthly payments"""
        credit_params = {
            "Credit amount": 200000,
            "Credit rate": [4.0],
            "Expected inflation": [2.0],
        }
        results = calculate_credit(credit_params)

        # 30-year payment should be less than 15-year payment
        self.assertLess(results[30]["monthly_payment"], results[15]["monthly_payment"])

    def test_higher_rate_higher_payment(self):
        """Test that higher interest rates result in higher payments"""
        low_rate_params = {
            "Credit amount": 100000,
            "Credit rate": [3.0],
            "Expected inflation": [0.0],
        }
        high_rate_params = {
            "Credit amount": 100000,
            "Credit rate": [7.0],
            "Expected inflation": [0.0],
        }

        low_results = calculate_credit(low_rate_params)
        high_results = calculate_credit(high_rate_params)

        # Higher rate should result in higher monthly payment
        self.assertLess(
            low_results[15]["monthly_payment"], high_results[15]["monthly_payment"]
        )


if __name__ == "__main__":
    unittest.main()
