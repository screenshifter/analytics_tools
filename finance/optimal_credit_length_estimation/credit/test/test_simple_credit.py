import unittest
import math
from ..simple_credit import calculate_credit, calculate_credit_with_overpayment


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


class TestCreditWithOverpayment(unittest.TestCase):
    
    def setUp(self):
        self.test_params = {
            "Credit amount": 100000,
            "Credit rate": [5.0],
            "Expected inflation": [2.0],
            "Acceptable monthly payment": [1000],
            "Investment interest rate": [4.0]
        }
    
    def test_no_overpayment_scenario(self):
        """Test when acceptable payment is lower than required payment"""
        params = self.test_params.copy()
        params["Acceptable monthly payment"] = [500]
        
        results = calculate_credit_with_overpayment(params)
        
        # Should have results for all years
        self.assertEqual(len(results), 28)
        
        # Check that actual_months field is present
        for year, data in results.items():
            self.assertIn("actual_months", data)
            self.assertIn("monthly_payment", data)
            self.assertIn("total_cost", data)
            self.assertIn("total_cost_adjusted", data)
            self.assertIn("investment_balance", data)
            # Investment balance should be 0 when no overpayment is possible
            self.assertEqual(data["investment_balance"], 0)
    
    def test_with_overpayment_scenario(self):
        """Test when overpayment reduces loan term"""
        params = self.test_params.copy()
        params["Acceptable monthly payment"] = [2000]
        
        results = calculate_credit_with_overpayment(params)
        standard_results = calculate_credit(params)
        
        # With overpayment, actual months should be less than standard for longer terms
        long_term_year = 20
        self.assertLessEqual(results[long_term_year]["actual_months"], long_term_year * 12)
        
        # Monthly payment should equal acceptable payment when overpayment occurs
        if standard_results[long_term_year]["monthly_payment"] < params["Acceptable monthly payment"][0]:
            self.assertEqual(results[long_term_year]["monthly_payment"], params["Acceptable monthly payment"][0])
            # Investment balance should be positive when credit is paid off early
            self.assertGreater(results[long_term_year]["investment_balance"], 0)
    
    def test_overpayment_reduces_total_cost(self):
        """Test that overpayment reduces total interest paid"""
        params = self.test_params.copy()
        params["Acceptable monthly payment"] = [1500]
        
        overpayment_results = calculate_credit_with_overpayment(params)
        standard_results = calculate_credit(params)
        
        # For longer terms, overpayment should reduce total cost
        year = 25
        if standard_results[year]["monthly_payment"] < params["Acceptable monthly payment"][0]:
            self.assertLess(overpayment_results[year]["total_cost"], standard_results[year]["total_cost"])


if __name__ == "__main__":
    unittest.main()
