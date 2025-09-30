import unittest
import math
from ..simple_credit import (
    calculate_credit,
    calculate_credit_with_overpayment,
    calculate_credit_with_investment,
)


class TestSimpleCreditCalculation(unittest.TestCase):
    """
    Unit tests for calculate_credit function using equivalence class partitioning.

    Test Categories:
    - Basic functionality: Known calculations, zero interest, inflation adjustment
    - Input ranges: Zero, small, large credit amounts
    - Interest rate classes: 0%, near-zero, low, medium, high (>15%)
    - Inflation rate classes: Zero, low, medium (3-10%), high (>10%), negative
    - Behavioral relationships: Term vs payment, rate vs payment
    - Output structure: Required fields, investment balance always zero

    Method: Boundary value analysis + equivalence class partitioning
    """

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

    def test_zero_credit_amount(self):
        """Test calculation with zero credit amount"""
        credit_params = {
            "Credit amount": 0,
            "Credit rate": [5.0],
            "Expected inflation": [2.0],
        }
        results = calculate_credit(credit_params)

        # All payments and costs should be zero
        for year, data in results.items():
            self.assertEqual(data["monthly_payment"], 0)
            self.assertEqual(data["total_cost"], 0)
            self.assertEqual(data["total_cost_adjusted"], 0)

    def test_high_interest_rate(self):
        """Test calculation with high interest rate (>15%)"""
        credit_params = {
            "Credit amount": 100000,
            "Credit rate": [20.0],
            "Expected inflation": [2.0],
        }
        results = calculate_credit(credit_params)

        # High rate should result in very high monthly payments
        result_10y = results[10]
        self.assertGreater(result_10y["monthly_payment"], 1500)
        self.assertGreater(result_10y["total_cost"], 180000)

    def test_medium_inflation_rate(self):
        """Test calculation with medium inflation rate (3% < rate <= 10%)"""
        credit_params = {
            "Credit amount": 100000,
            "Credit rate": [5.0],
            "Expected inflation": [7.0],
        }
        results = calculate_credit(credit_params)

        result_10y = results[10]
        # With 7% inflation, adjusted cost should be significantly lower
        inflation_factor = (1 + 0.07) ** 10
        expected_adjusted = result_10y["total_cost"] / inflation_factor
        self.assertAlmostEqual(
            result_10y["total_cost_adjusted"], expected_adjusted, places=2
        )
        self.assertLess(
            result_10y["total_cost_adjusted"], result_10y["total_cost"] * 0.6
        )

    def test_high_inflation_rate(self):
        """Test calculation with high inflation rate (>10%)"""
        credit_params = {
            "Credit amount": 100000,
            "Credit rate": [5.0],
            "Expected inflation": [15.0],
        }
        results = calculate_credit(credit_params)

        result_10y = results[10]
        # With 15% inflation, adjusted cost should be much lower
        self.assertLess(
            result_10y["total_cost_adjusted"], result_10y["total_cost"] * 0.3
        )

    def test_negative_inflation_deflation(self):
        """Test calculation with negative inflation (deflation)"""
        credit_params = {
            "Credit amount": 100000,
            "Credit rate": [5.0],
            "Expected inflation": [-2.0],
        }
        results = calculate_credit(credit_params)

        result_10y = results[10]
        # With deflation, adjusted cost should be higher than nominal
        self.assertGreater(result_10y["total_cost_adjusted"], result_10y["total_cost"])

    def test_very_small_credit_amount(self):
        """Test calculation with very small credit amount"""
        credit_params = {
            "Credit amount": 0.5,
            "Credit rate": [5.0],
            "Expected inflation": [2.0],
        }
        results = calculate_credit(credit_params)

        # Should handle small amounts without errors
        result_10y = results[10]
        self.assertGreater(result_10y["monthly_payment"], 0)
        self.assertLess(result_10y["monthly_payment"], 10)

    def test_very_large_credit_amount(self):
        """Test calculation with very large credit amount"""
        credit_params = {
            "Credit amount": 10000000,  # 10 million
            "Credit rate": [5.0],
            "Expected inflation": [2.0],
        }
        results = calculate_credit(credit_params)

        # Should handle large amounts proportionally
        result_10y = results[10]
        self.assertGreater(result_10y["monthly_payment"], 100000)
        self.assertGreater(result_10y["total_cost"], 10000000)

    def test_very_small_interest_rate(self):
        """Test calculation with very small positive interest rate"""
        credit_params = {
            "Credit amount": 100000,
            "Credit rate": [0.01],  # 0.01%
            "Expected inflation": [2.0],
        }
        results = calculate_credit(credit_params)

        result_10y = results[10]
        # Very low rate should result in payment close to zero-interest case
        zero_interest_payment = 100000 / (10 * 12)
        self.assertAlmostEqual(
            result_10y["monthly_payment"], zero_interest_payment, delta=10
        )

    def test_investment_balance_always_zero(self):
        """Test that investment balance is always zero for calculate_credit"""
        credit_params = {
            "Credit amount": 100000,
            "Credit rate": [5.0],
            "Expected inflation": [2.0],
        }
        results = calculate_credit(credit_params)

        # Investment balance should always be 0 for basic credit calculation
        for year, data in results.items():
            self.assertEqual(data["investment_balance"], 0)


class TestCreditWithOverpayment(unittest.TestCase):
    """
    Unit tests for calculate_credit_with_overpayment function using equivalence class partitioning.

    Test Categories:
    - Payment scenarios: Below required, equal, above required payment
    - Overpayment behavior: Early payoff, investment calculation, cost adjustment
    - Input ranges: Zero, small, large amounts and rates
    - Investment rates: Zero, low, medium, high vs credit rate
    - Inflation impact: Zero, positive, negative with overpayment
    - Edge cases: Extreme values, boundary conditions

    Method: Boundary value analysis + equivalence class partitioning
    """

    def setUp(self):
        self.test_params = {
            "Credit amount": 100000,
            "Credit rate": [5.0],
            "Expected inflation": [2.0],
            "Acceptable monthly payment": [1000],
            "Investment interest rate": [4.0],
        }

    def test_no_overpayment_scenario(self):
        """Test when acceptable payment is lower than required payment"""
        params = self.test_params.copy()
        params["Acceptable monthly payment"] = [500]

        results = calculate_credit_with_overpayment(params)

        # Should have results for all years
        self.assertEqual(len(results), 28)

        # Check that required fields are present
        for year, data in results.items():
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

        # With overpayment, results should be calculated
        long_term_year = 20
        self.assertIn(long_term_year, results)

        # Monthly payment should equal acceptable payment when overpayment occurs
        if (
            standard_results[long_term_year]["monthly_payment"]
            < params["Acceptable monthly payment"][0]
        ):
            self.assertEqual(
                results[long_term_year]["monthly_payment"],
                params["Acceptable monthly payment"][0],
            )
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
        if (
            standard_results[year]["monthly_payment"]
            < params["Acceptable monthly payment"][0]
        ):
            self.assertLess(
                overpayment_results[year]["total_cost"],
                standard_results[year]["total_cost"],
            )

    def test_zero_acceptable_payment(self):
        """Test with zero acceptable payment"""
        params = self.test_params.copy()
        params["Acceptable monthly payment"] = [0]

        results = calculate_credit_with_overpayment(params)
        standard_results = calculate_credit(params)

        # Should use required payment when acceptable is zero
        for year, data in results.items():
            self.assertEqual(
                data["monthly_payment"], standard_results[year]["monthly_payment"]
            )
            self.assertEqual(data["investment_balance"], 0)

    def test_high_investment_rate(self):
        """Test with high investment rate (>10%)"""
        params = self.test_params.copy()
        params["Acceptable monthly payment"] = [2000]
        params["Investment interest rate"] = [15.0]  # High investment rate

        results = calculate_credit_with_overpayment(params)

        # High investment rate should generate significant investment balance
        long_term = 25
        if results[long_term]["investment_balance"] > 0:
            self.assertGreater(results[long_term]["investment_balance"], 50000)

    def test_investment_rate_vs_credit_rate(self):
        """Test when investment rate is higher than credit rate"""
        params = self.test_params.copy()
        params["Credit rate"] = [3.0]  # Low credit rate
        params["Investment interest rate"] = [8.0]  # High investment rate
        params["Acceptable monthly payment"] = [1500]

        results = calculate_credit_with_overpayment(params)

        # When investment rate > credit rate, total cost should be significantly reduced
        long_term = 20
        if results[long_term]["investment_balance"] > 0:
            self.assertLess(
                results[long_term]["total_cost"], 0
            )  # Could be negative (profit)

    def test_zero_investment_rate(self):
        """Test with zero investment rate"""
        params = self.test_params.copy()
        params["Acceptable monthly payment"] = [1500]
        params["Investment interest rate"] = [0.0]

        results = calculate_credit_with_overpayment(params)
        standard_results = calculate_credit(params)

        # With zero investment rate, should still reduce cost due to early payoff
        long_term = 25
        if (
            standard_results[long_term]["monthly_payment"]
            < params["Acceptable monthly payment"][0]
        ):
            self.assertLessEqual(
                results[long_term]["total_cost"],
                standard_results[long_term]["total_cost"],
            )

    def test_extreme_overpayment(self):
        """Test with very high acceptable payment"""
        params = self.test_params.copy()
        params["Acceptable monthly payment"] = [10000]  # Very high payment

        results = calculate_credit_with_overpayment(params)

        # Should pay off quickly and generate large investment balance
        long_term = 30
        self.assertEqual(results[long_term]["monthly_payment"], 10000)
        self.assertGreater(results[long_term]["investment_balance"], 100000)

    def test_negative_inflation_with_overpayment(self):
        """Test overpayment with deflation"""
        params = self.test_params.copy()
        params["Expected inflation"] = [-2.0]  # Deflation
        params["Acceptable monthly payment"] = [1500]

        results = calculate_credit_with_overpayment(params)

        # With deflation, adjusted cost should be higher than nominal
        long_term = 20
        if results[long_term]["total_cost"] > 0:
            self.assertGreater(
                results[long_term]["total_cost_adjusted"],
                results[long_term]["total_cost"],
            )

    def test_equal_acceptable_payment(self):
        """Test when acceptable payment exactly equals required payment"""
        params = self.test_params.copy()
        standard_results = calculate_credit(params)

        # Set acceptable payment equal to 15-year required payment
        params["Acceptable monthly payment"] = [standard_results[15]["monthly_payment"]]

        results = calculate_credit_with_overpayment(params)

        # For 15-year term, should match standard calculation
        self.assertEqual(
            results[15]["monthly_payment"], standard_results[15]["monthly_payment"]
        )
        self.assertEqual(results[15]["total_cost"], standard_results[15]["total_cost"])
        self.assertEqual(results[15]["investment_balance"], 0)

    def test_small_credit_amount_overpayment(self):
        """Test overpayment with small credit amount"""
        params = self.test_params.copy()
        params["Credit amount"] = 1000  # Small amount
        params["Acceptable monthly payment"] = [500]  # High relative to amount

        results = calculate_credit_with_overpayment(params)

        # Should pay off very quickly
        short_term = 5
        self.assertEqual(results[short_term]["monthly_payment"], 500)
        self.assertGreater(results[short_term]["investment_balance"], 0)


class TestCreditWithInvestment(unittest.TestCase):
    """
    Unit tests for calculate_credit_with_investment function using equivalence class partitioning.

    Test Categories:
    - Payment scenarios: Below required, equal, above required payment
    - Investment behavior: Payment difference investment, cost reduction
    - Investment rates: Zero, low, medium, high vs credit rate
    - Inflation impact: Zero, positive, negative with investment
    - Edge cases: Extreme values, boundary conditions
    - Output consistency: Required fields, proper calculations

    Method: Boundary value analysis + equivalence class partitioning
    """

    def setUp(self):
        self.credit_parameters = {
            "Credit amount": 100000,
            "Credit rate": [5.0],
            "Expected inflation": [3.0],
            "Acceptable monthly payment": [1000],
            "Investment interest rate": [7.0],
        }

    def test_monthly_payment_never_below_credit(self):
        """Test that monthly payment is never below required credit payment"""
        test_params = self.credit_parameters.copy()
        results = calculate_credit_with_investment(test_params)
        credit_results = calculate_credit(test_params)

        for years, data in results.items():
            self.assertGreaterEqual(
                data["monthly_payment"], credit_results[years]["monthly_payment"]
            )

    def test_low_acceptable_payment(self):
        """Test that when acceptable payment is too low, credit payment is used"""
        test_params = self.credit_parameters.copy()
        test_params["Acceptable monthly payment"] = [200]
        results = calculate_credit_with_investment(test_params)
        credit_results = calculate_credit(test_params)

        # Monthly payment should equal credit payment (no investment possible)
        for years, data in results.items():
            self.assertEqual(
                data["monthly_payment"], credit_results[years]["monthly_payment"]
            )
            self.assertEqual(data["total_cost"], credit_results[years]["total_cost"])

    def test_total_cost_reduction(self):
        """Test that total cost is reduced when investment is possible"""
        test_params = self.credit_parameters.copy()
        results = calculate_credit_with_investment(test_params)
        credit_results = calculate_credit(test_params)

        # Find a case where investment is possible
        for years in [10, 15, 20]:
            if (
                credit_results[years]["monthly_payment"]
                < test_params["Acceptable monthly payment"][0]
            ):
                self.assertLess(
                    results[years]["total_cost"],
                    credit_results[years]["total_cost"],
                )

    def test_zero_investment_rate(self):
        """Test with zero investment rate"""
        test_params = self.credit_parameters.copy()
        test_params["Investment interest rate"] = [0.0]
        results = calculate_credit_with_investment(test_params)
        credit_results = calculate_credit(test_params)

        for years, data in results.items():
            expected_payment = max(
                test_params["Acceptable monthly payment"][0],
                credit_results[years]["monthly_payment"],
            )
            self.assertEqual(data["monthly_payment"], expected_payment)

    def test_exact_payment_match(self):
        """Test when acceptable payment exactly matches credit payment"""
        credit_results = calculate_credit(self.credit_parameters)
        exact_payment = credit_results[10]["monthly_payment"]
        test_params = self.credit_parameters.copy()
        test_params["Acceptable monthly payment"] = [exact_payment]
        results = calculate_credit_with_investment(test_params)

        # Monthly payment and total cost should be unchanged for this term
        self.assertEqual(results[10]["monthly_payment"], exact_payment)
        self.assertEqual(results[10]["total_cost"], credit_results[10]["total_cost"])
        self.assertEqual(
            results[10]["total_cost_adjusted"],
            credit_results[10]["total_cost_adjusted"],
        )

    def test_inflation_adjustment_calculation(self):
        """Test that inflation adjustment is calculated correctly"""
        test_params = self.credit_parameters.copy()
        results = calculate_credit_with_investment(test_params)
        credit_results = calculate_credit(test_params)

        # Test specific case where we can verify calculation
        years = 10
        acceptable_payment = test_params["Acceptable monthly payment"][0]
        investment_rate = test_params["Investment interest rate"][0]
        inflation_rate = test_params["Expected inflation"][0]
        if credit_results[years]["monthly_payment"] < acceptable_payment:
            # Calculate expected values manually
            monthly_investment = (
                acceptable_payment - credit_results[years]["monthly_payment"]
            )
            from detail.investment import calculate_simple_investment

            investment_balance = calculate_simple_investment(
                0, monthly_investment, investment_rate, years
            )
            expected_total_cost = (
                credit_results[years]["total_cost"] - investment_balance
            )
            inflation_factor = (1 + inflation_rate / 100) ** years
            expected_adjusted_cost = round(expected_total_cost / inflation_factor, 2)

            self.assertEqual(
                results[years]["total_cost_adjusted"], expected_adjusted_cost
            )

    def test_inflation_adjustment_with_zero_inflation(self):
        """Test inflation adjustment with zero inflation rate"""
        test_params = self.credit_parameters.copy()
        test_params["Expected inflation"] = [0.0]
        results = calculate_credit_with_investment(test_params)

        # With zero inflation, adjusted cost should equal nominal cost
        for years, data in results.items():
            self.assertAlmostEqual(
                data["total_cost_adjusted"], data["total_cost"], places=2
            )

    def test_inflation_adjustment_reduces_cost(self):
        """Test that inflation adjustment reduces the adjusted cost when cost is positive"""
        test_params = self.credit_parameters.copy()
        results = calculate_credit_with_investment(test_params)

        # For positive costs, adjusted cost should be less than nominal cost
        # For negative costs (profit), adjusted cost should be greater than nominal cost
        for years, data in results.items():
            if years > 1 and data["total_cost"] > 0:
                self.assertLess(data["total_cost_adjusted"], data["total_cost"])
            elif years > 1 and data["total_cost"] < 0:
                self.assertGreater(data["total_cost_adjusted"], data["total_cost"])

    def test_medium_investment_rate(self):
        """Test with medium investment rate (5-10%)"""
        test_params = self.credit_parameters.copy()
        test_params["Investment interest rate"] = [8.0]  # Medium investment rate
        results = calculate_credit_with_investment(test_params)
        credit_results = calculate_credit(test_params)

        # Medium investment rate should provide reasonable returns
        acceptable_payment = test_params["Acceptable monthly payment"][0]
        for years, data in results.items():
            if credit_results[years]["monthly_payment"] < acceptable_payment:
                self.assertGreater(data["investment_balance"], 0)

    def test_high_investment_rate(self):
        """Test with high investment rate (>10%)"""
        test_params = self.credit_parameters.copy()
        test_params["Investment interest rate"] = [15.0]  # High investment rate
        results = calculate_credit_with_investment(test_params)
        credit_results = calculate_credit(test_params)

        # High investment rate should generate significant returns
        long_term = 20
        acceptable_payment = test_params["Acceptable monthly payment"][0]
        if credit_results[long_term]["monthly_payment"] < acceptable_payment:
            self.assertGreater(results[long_term]["investment_balance"], 50000)

    def test_investment_rate_equals_credit_rate(self):
        """Test when investment rate equals credit rate"""
        test_params = self.credit_parameters.copy()
        test_params["Investment interest rate"] = [5.0]  # Same as credit rate
        results = calculate_credit_with_investment(test_params)
        credit_results = calculate_credit(test_params)

        # When rates are equal, investment should still provide some benefit
        acceptable_payment = test_params["Acceptable monthly payment"][0]
        for years, data in results.items():
            if credit_results[years]["monthly_payment"] < acceptable_payment:
                self.assertGreaterEqual(data["investment_balance"], 0)

    def test_large_payment_difference(self):
        """Test with very large acceptable payment creating big investment difference"""
        test_params = self.credit_parameters.copy()
        test_params["Acceptable monthly payment"] = [3000]  # Much higher than required
        results = calculate_credit_with_investment(test_params)
        credit_results = calculate_credit(test_params)

        # Large payment difference should create substantial investment balance
        long_term = 25
        self.assertGreater(results[long_term]["investment_balance"], 100000)
        # Total cost should be significantly reduced or negative
        self.assertLess(
            results[long_term]["total_cost"],
            credit_results[long_term]["total_cost"] * 0.5,
        )

    def test_negative_inflation_with_investment(self):
        """Test investment calculation with deflation"""
        test_params = self.credit_parameters.copy()
        test_params["Expected inflation"] = [-2.0]  # Deflation
        results = calculate_credit_with_investment(test_params)

        # With deflation, adjusted cost should be higher than nominal
        for years, data in results.items():
            if years > 1 and data["total_cost"] > 0:
                self.assertGreater(data["total_cost_adjusted"], data["total_cost"])

    def test_high_inflation_with_investment(self):
        """Test investment calculation with high inflation (>10%)"""
        test_params = self.credit_parameters.copy()
        test_params["Expected inflation"] = [12.0]  # High inflation
        results = calculate_credit_with_investment(test_params)

        # With high inflation, adjusted cost should be much lower
        long_term = 20
        if results[long_term]["total_cost"] > 0:
            self.assertLess(
                results[long_term]["total_cost_adjusted"],
                results[long_term]["total_cost"] * 0.4,
            )

    def test_zero_credit_results(self):
        """Test with zero credit amounts in input results"""
        test_params = self.credit_parameters.copy()
        test_params["Credit amount"] = 0
        results = calculate_credit_with_investment(test_params)

        # With zero credit, should use acceptable payment for investment
        acceptable_payment = test_params["Acceptable monthly payment"][0]
        for years, data in results.items():
            self.assertEqual(data["monthly_payment"], acceptable_payment)
            self.assertGreater(data["investment_balance"], 0)

    def test_investment_vs_credit_rate_comparison(self):
        """Test comparison when investment rate is much higher than credit rate"""
        test_params = self.credit_parameters.copy()
        test_params["Acceptable monthly payment"] = [1500]
        test_params["Investment interest rate"] = [
            12.0
        ]  # Much higher than typical credit rate
        results = calculate_credit_with_investment(test_params)
        credit_results = calculate_credit(test_params)

        # High investment rate should make total cost negative (profit)
        long_term = 25
        if credit_results[long_term]["monthly_payment"] < 1500:
            self.assertLess(results[long_term]["total_cost"], 0)

    def test_output_structure_consistency(self):
        """Test that all required output fields are present and properly typed"""
        test_params = self.credit_parameters.copy()
        results = calculate_credit_with_investment(test_params)

        # Verify all required fields are present and properly typed
        for years, data in results.items():
            self.assertIn("monthly_payment", data)
            self.assertIn("total_cost", data)
            self.assertIn("total_cost_adjusted", data)
            self.assertIn("investment_balance", data)
            self.assertIsInstance(data["monthly_payment"], (int, float))
            self.assertIsInstance(data["total_cost"], (int, float))
            self.assertIsInstance(data["total_cost_adjusted"], (int, float))
            self.assertIsInstance(data["investment_balance"], (int, float))


if __name__ == "__main__":
    unittest.main()
