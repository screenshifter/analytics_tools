import unittest
from ..investment import calculate_simple_investment


class TestInvestmentCalculation(unittest.TestCase):
    """
    Unit tests for calculate_simple_investment function using equivalence class partitioning.

    Test Categories:
    - Initial investment classes: Zero, small, medium, large amounts
    - Monthly income classes: Zero, small, medium, large amounts
    - Interest rate classes: Zero, very low (<1%), low (1-5%), medium (5-10%), high (>10%)
    - Time period classes: Very short (<1 year), short (1-5 years), medium (5-15 years), long (>15 years)
    - Input validation: Negative values, zero/negative years
    - Behavioral relationships: Rate vs return, time vs return, contribution vs return
    - Edge cases: Extreme values, precision handling
    - Output validation: Return type, precision, mathematical correctness

    Method: Boundary value analysis + equivalence class partitioning
    """

    def test_zero_interest_rate(self):
        """Test calculation with zero interest rate"""
        result = calculate_simple_investment(10000, 500, 0.0, 5)
        expected = 10000 + (500 * 5 * 12)  # Initial + monthly contributions
        self.assertEqual(result, expected)

    def test_zero_initial_investment(self):
        """Test calculation with zero initial investment"""
        result = calculate_simple_investment(0, 1000, 6.0, 10)
        # Only monthly contributions with compound interest
        monthly_rate = 0.06 / 12
        months = 120
        expected = 1000 * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        self.assertAlmostEqual(result, round(expected, 2), places=2)

    def test_zero_monthly_income(self):
        """Test calculation with zero monthly contributions"""
        result = calculate_simple_investment(50000, 0, 5.0, 10)
        # Only initial investment with compound interest
        expected = 50000 * ((1 + 0.05 / 12) ** (10 * 12))
        self.assertAlmostEqual(result, round(expected, 2), places=2)

    def test_zero_years(self):
        """Test calculation with zero investment period raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_simple_investment(25000, 1000, 7.0, 0)

    def test_all_zeros_except_years(self):
        """Test calculation with zero initial and monthly but positive years"""
        result = calculate_simple_investment(0, 0, 0.0, 5)
        self.assertEqual(result, 0.0)

    def test_basic_calculation(self):
        """Test basic investment calculation with known values"""
        # 10,000 initial + 500/month for 5 years at 6% annual
        result = calculate_simple_investment(10000, 500, 6.0, 5)

        # Manual calculation for verification
        monthly_rate = 0.06 / 12
        months = 60
        initial_fv = 10000 * ((1 + monthly_rate) ** months)
        annuity_fv = 500 * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        expected = round(initial_fv + annuity_fv, 2)

        self.assertEqual(result, expected)

    def test_higher_rate_higher_return(self):
        """Test that higher interest rates produce higher returns"""
        low_rate = calculate_simple_investment(10000, 500, 3.0, 10)
        high_rate = calculate_simple_investment(10000, 500, 8.0, 10)
        self.assertLess(low_rate, high_rate)

    def test_longer_period_higher_return(self):
        """Test that longer investment periods produce higher returns"""
        short_period = calculate_simple_investment(10000, 500, 6.0, 5)
        long_period = calculate_simple_investment(10000, 500, 6.0, 15)
        self.assertLess(short_period, long_period)

    def test_higher_monthly_higher_return(self):
        """Test that higher monthly contributions produce higher returns"""
        low_monthly = calculate_simple_investment(10000, 300, 6.0, 10)
        high_monthly = calculate_simple_investment(10000, 800, 6.0, 10)
        self.assertLess(low_monthly, high_monthly)

    def test_compound_effect(self):
        """Test that compound interest produces exponential growth"""
        # Compare simple vs compound interest effect
        result_1_year = calculate_simple_investment(10000, 0, 10.0, 1)
        result_2_years = calculate_simple_investment(10000, 0, 10.0, 2)

        # Growth should be more than linear due to compounding
        first_year_growth = result_1_year - 10000
        second_year_growth = result_2_years - result_1_year
        self.assertGreater(second_year_growth, first_year_growth)

    def test_return_type_and_precision(self):
        """Test that function returns float with proper precision"""
        result = calculate_simple_investment(10000.123, 500.456, 6.789, 5)
        self.assertIsInstance(result, float)
        # Check that result is rounded to 2 decimal places
        self.assertEqual(result, round(result, 2))

    def test_negative_initial_investment(self):
        """Test that negative initial investment raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_simple_investment(-1000, 500, 5.0, 10)

    def test_negative_monthly_income(self):
        """Test that negative monthly income raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_simple_investment(10000, -500, 5.0, 10)

    def test_negative_interest_rate(self):
        """Test that negative interest rate raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_simple_investment(10000, 500, -2.0, 10)

    def test_negative_years(self):
        """Test that negative years raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_simple_investment(10000, 500, 5.0, -5)

    def test_very_low_interest_rate(self):
        """Test calculation with very low interest rate (<1%)"""
        result = calculate_simple_investment(10000, 500, 0.5, 10)
        # Should be close to zero-interest case but slightly higher
        zero_interest = 10000 + (500 * 10 * 12)
        self.assertGreater(result, zero_interest)
        self.assertLess(result, zero_interest * 1.1)

    def test_low_interest_rate(self):
        """Test calculation with low interest rate (1-5%)"""
        result = calculate_simple_investment(10000, 500, 3.0, 10)
        # Should provide moderate growth
        self.assertGreater(result, 70000)
        self.assertLess(result, 90000)

    def test_medium_interest_rate(self):
        """Test calculation with medium interest rate (5-10%)"""
        result = calculate_simple_investment(10000, 500, 7.0, 10)
        # Should provide good growth
        self.assertGreater(result, 85000)
        self.assertLess(result, 110000)

    def test_high_interest_rate(self):
        """Test calculation with high interest rate (>10%)"""
        result = calculate_simple_investment(10000, 500, 15.0, 10)
        # Should provide significant growth
        self.assertGreater(result, 120000)

    def test_small_initial_investment(self):
        """Test calculation with small initial investment (<1000)"""
        result = calculate_simple_investment(100, 500, 6.0, 10)
        # Monthly contributions should dominate
        monthly_only = calculate_simple_investment(0, 500, 6.0, 10)
        self.assertAlmostEqual(result, monthly_only, delta=500)

    def test_medium_initial_investment(self):
        """Test calculation with medium initial investment (1000-50000)"""
        result = calculate_simple_investment(25000, 500, 6.0, 10)
        # Both components should contribute significantly
        self.assertGreater(result, 80000)
        self.assertLess(result, 130000)

    def test_large_initial_investment(self):
        """Test calculation with large initial investment (>50000)"""
        result = calculate_simple_investment(100000, 500, 6.0, 10)
        # Initial investment should dominate
        initial_only = calculate_simple_investment(100000, 0, 6.0, 10)
        self.assertLess(result - initial_only, 85000)

    def test_small_monthly_income(self):
        """Test calculation with small monthly income (<100)"""
        result = calculate_simple_investment(10000, 50, 6.0, 10)
        # Initial investment should dominate
        initial_only = calculate_simple_investment(10000, 0, 6.0, 10)
        self.assertLess(result - initial_only, 10000)

    def test_medium_monthly_income(self):
        """Test calculation with medium monthly income (100-1000)"""
        result = calculate_simple_investment(10000, 500, 6.0, 10)
        # Both components should be significant
        self.assertGreater(result, 70000)
        self.assertLess(result, 105000)

    def test_large_monthly_income(self):
        """Test calculation with large monthly income (>1000)"""
        result = calculate_simple_investment(10000, 2000, 6.0, 10)
        # Monthly contributions should dominate
        monthly_only = calculate_simple_investment(0, 2000, 6.0, 10)
        self.assertLess(abs(result - monthly_only), 30000)

    def test_very_short_period(self):
        """Test calculation with very short period (<1 year)"""
        result = calculate_simple_investment(10000, 500, 6.0, 0.5)
        # Limited compounding effect
        self.assertGreater(result, 13000)
        self.assertLess(result, 14000)

    def test_short_period(self):
        """Test calculation with short period (1-5 years)"""
        result = calculate_simple_investment(10000, 500, 6.0, 3)
        # Moderate compounding
        self.assertGreater(result, 25000)
        self.assertLess(result, 35000)

    def test_medium_period(self):
        """Test calculation with medium period (5-15 years)"""
        result = calculate_simple_investment(10000, 500, 6.0, 10)
        # Significant compounding
        self.assertGreater(result, 70000)
        self.assertLess(result, 105000)

    def test_long_period(self):
        """Test calculation with long period (>15 years)"""
        result = calculate_simple_investment(10000, 500, 6.0, 20)
        # Strong compounding effect
        self.assertGreater(result, 200000)

    def test_very_small_amounts(self):
        """Test calculation with very small amounts"""
        result = calculate_simple_investment(1, 1, 5.0, 1)
        # Should handle small amounts without errors
        self.assertGreater(result, 10)
        self.assertLess(result, 20)

    def test_very_large_amounts(self):
        """Test calculation with very large amounts"""
        result = calculate_simple_investment(1000000, 10000, 6.0, 10)
        # Should handle large amounts proportionally
        self.assertGreater(result, 2500000)

    def test_fractional_years(self):
        """Test calculation with fractional years"""
        result = calculate_simple_investment(10000, 500, 6.0, 2.5)
        # Should handle fractional periods correctly
        self.assertGreater(result, 20000)
        self.assertLess(result, 30000)

    def test_mathematical_consistency(self):
        """Test mathematical consistency of compound interest formula"""
        # Test that doubling time period roughly doubles the growth
        result_5y = calculate_simple_investment(10000, 0, 6.0, 5)
        result_10y = calculate_simple_investment(10000, 0, 6.0, 10)

        growth_5y = result_5y - 10000
        growth_10y = result_10y - 10000

        # 10-year growth should be more than double 5-year growth due to compounding
        self.assertGreater(growth_10y, growth_5y * 2)

    def test_annuity_formula_accuracy(self):
        """Test accuracy of annuity calculation component"""
        # Test pure annuity (no initial investment)
        result = calculate_simple_investment(0, 1000, 12.0, 10)

        # Manual calculation using annuity formula
        monthly_rate = 0.12 / 12
        months = 120
        expected = 1000 * (((1 + monthly_rate) ** months - 1) / monthly_rate)

        self.assertAlmostEqual(result, round(expected, 2), places=2)


if __name__ == "__main__":
    unittest.main()
