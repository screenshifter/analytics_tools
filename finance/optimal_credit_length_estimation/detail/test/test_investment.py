import unittest
from ..investment import calculate_simple_investment


class TestInvestmentCalculation(unittest.TestCase):

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
        """Test calculation with zero investment period"""
        result = calculate_simple_investment(25000, 1000, 7.0, 0)
        self.assertEqual(result, 25000)  # Only initial investment, no time to grow

    def test_all_zeros(self):
        """Test calculation with all zero inputs"""
        result = calculate_simple_investment(0, 0, 0.0, 0)
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


if __name__ == "__main__":
    unittest.main()
