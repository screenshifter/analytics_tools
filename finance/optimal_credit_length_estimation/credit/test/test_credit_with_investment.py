import unittest
from credit.credit_with_investment import calculate_credit_with_investment
from credit.simple_credit import calculate_credit


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
    
    Method: Boundary value analysis + equivalence partitioning
    """
    
    def setUp(self):
        self.credit_parameters = {
            "Credit amount": 100000,
            "Credit rate": [5.0],
            "Expected inflation": [3.0]
        }
        self.credit_results = calculate_credit(self.credit_parameters)
        self.acceptable_payment = 1000
        self.investment_rate = 7.0
        self.inflation_rate = 3.0
    
    def test_monthly_payment_never_below_credit(self):
        """Test that monthly payment is never below required credit payment"""
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [self.investment_rate],
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        for years, data in results.items():
            self.assertGreaterEqual(data['monthly_payment'], self.credit_results[years]['monthly_payment'])
    
    def test_low_acceptable_payment(self):
        """Test that when acceptable payment is too low, credit payment is used"""
        test_params = {
            "Acceptable monthly payment": [200],
            "Investment interest rate": [self.investment_rate],
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # Monthly payment should equal credit payment (no investment possible)
        for years, data in results.items():
            self.assertEqual(data['monthly_payment'], self.credit_results[years]['monthly_payment'])
            self.assertEqual(data['total_cost'], self.credit_results[years]['total_cost'])
    
    def test_total_cost_reduction(self):
        """Test that total cost is reduced when investment is possible"""
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [self.investment_rate],
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # Find a case where investment is possible
        for years in [10, 15, 20]:
            if self.credit_results[years]['monthly_payment'] < self.acceptable_payment:
                self.assertLess(
                    results[years]['total_cost'],
                    self.credit_results[years]['total_cost']
                )
    
    def test_zero_investment_rate(self):
        """Test with zero investment rate"""
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [0.0],
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        for years, data in results.items():
            expected_payment = max(self.acceptable_payment, self.credit_results[years]['monthly_payment'])
            self.assertEqual(data['monthly_payment'], expected_payment)
    
    def test_exact_payment_match(self):
        """Test when acceptable payment exactly matches credit payment"""
        exact_payment = self.credit_results[10]['monthly_payment']
        test_params = {
            "Acceptable monthly payment": [exact_payment],
            "Investment interest rate": [self.investment_rate],
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # Monthly payment and total cost should be unchanged for this term
        self.assertEqual(results[10]['monthly_payment'], exact_payment)
        self.assertEqual(
            results[10]['total_cost'],
            self.credit_results[10]['total_cost']
        )
        self.assertEqual(
            results[10]['total_cost_adjusted'],
            self.credit_results[10]['total_cost_adjusted']
        )
    
    def test_inflation_adjustment_calculation(self):
        """Test that inflation adjustment is calculated correctly"""
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [self.investment_rate],
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # Test specific case where we can verify calculation
        years = 10
        if self.credit_results[years]['monthly_payment'] < self.acceptable_payment:
            # Calculate expected values manually
            monthly_investment = self.acceptable_payment - self.credit_results[years]['monthly_payment']
            investment_balance = calculate_simple_investment(
                0, monthly_investment, self.investment_rate, years
            )
            expected_total_cost = self.credit_results[years]['total_cost'] - investment_balance
            inflation_factor = (1 + self.inflation_rate / 100) ** years
            expected_adjusted_cost = round(expected_total_cost / inflation_factor, 2)
            
            self.assertEqual(results[years]['total_cost_adjusted'], expected_adjusted_cost)
    
    def test_inflation_adjustment_with_zero_inflation(self):
        """Test inflation adjustment with zero inflation rate"""
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [self.investment_rate],
            "Expected inflation": [0.0]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # With zero inflation, adjusted cost should equal nominal cost
        for years, data in results.items():
            self.assertAlmostEqual(data['total_cost_adjusted'], data['total_cost'], places=2)
    
    def test_inflation_adjustment_reduces_cost(self):
        """Test that inflation adjustment reduces the adjusted cost when cost is positive"""
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [self.investment_rate],
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # For positive costs, adjusted cost should be less than nominal cost
        # For negative costs (profit), adjusted cost should be greater than nominal cost
        for years, data in results.items():
            if years > 1 and data['total_cost'] > 0:
                self.assertLess(data['total_cost_adjusted'], data['total_cost'])
            elif years > 1 and data['total_cost'] < 0:
                self.assertGreater(data['total_cost_adjusted'], data['total_cost'])
    
    def test_medium_investment_rate(self):
        """Test with medium investment rate (5-10%)"""
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [8.0],  # Medium investment rate
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # Medium investment rate should provide reasonable returns
        for years, data in results.items():
            if self.credit_results[years]['monthly_payment'] < self.acceptable_payment:
                self.assertGreater(data['investment_balance'], 0)
    
    def test_high_investment_rate(self):
        """Test with high investment rate (>10%)"""
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [15.0],  # High investment rate
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # High investment rate should generate significant returns
        long_term = 20
        if self.credit_results[long_term]['monthly_payment'] < self.acceptable_payment:
            self.assertGreater(results[long_term]['investment_balance'], 50000)
    
    def test_investment_rate_equals_credit_rate(self):
        """Test when investment rate equals credit rate"""
        credit_rate = 5.0
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [credit_rate],  # Same as credit rate
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # When rates are equal, investment should still provide some benefit
        for years, data in results.items():
            if self.credit_results[years]['monthly_payment'] < self.acceptable_payment:
                self.assertGreaterEqual(data['investment_balance'], 0)
    
    def test_large_payment_difference(self):
        """Test with very large acceptable payment creating big investment difference"""
        test_params = {
            "Acceptable monthly payment": [3000],  # Much higher than required
            "Investment interest rate": [self.investment_rate],
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # Large payment difference should create substantial investment balance
        long_term = 25
        self.assertGreater(results[long_term]['investment_balance'], 100000)
        # Total cost should be significantly reduced or negative
        self.assertLess(results[long_term]['total_cost'], self.credit_results[long_term]['total_cost'] * 0.5)
    
    def test_negative_inflation_with_investment(self):
        """Test investment calculation with deflation"""
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [self.investment_rate],
            "Expected inflation": [-2.0]  # Deflation
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # With deflation, adjusted cost should be higher than nominal
        for years, data in results.items():
            if years > 1 and data['total_cost'] > 0:
                self.assertGreater(data['total_cost_adjusted'], data['total_cost'])
    
    def test_high_inflation_with_investment(self):
        """Test investment calculation with high inflation (>10%)"""
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [self.investment_rate],
            "Expected inflation": [12.0]  # High inflation
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # With high inflation, adjusted cost should be much lower
        long_term = 20
        if results[long_term]['total_cost'] > 0:
            self.assertLess(results[long_term]['total_cost_adjusted'], results[long_term]['total_cost'] * 0.4)
    
    def test_zero_credit_results(self):
        """Test with zero credit amounts in input results"""
        zero_credit_results = {years: {'monthly_payment': 0, 'total_cost': 0, 'total_cost_adjusted': 0, 'investment_balance': 0} for years in range(3, 31)}
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [self.investment_rate],
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(zero_credit_results, test_params)
        
        # With zero credit, should use acceptable payment for investment
        for years, data in results.items():
            self.assertEqual(data['monthly_payment'], self.acceptable_payment)
            self.assertGreater(data['investment_balance'], 0)
    
    def test_investment_vs_credit_rate_comparison(self):
        """Test comparison when investment rate is much higher than credit rate"""
        test_params = {
            "Acceptable monthly payment": [1500],
            "Investment interest rate": [12.0],  # Much higher than typical credit rate
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # High investment rate should make total cost negative (profit)
        long_term = 25
        if self.credit_results[long_term]['monthly_payment'] < 1500:
            self.assertLess(results[long_term]['total_cost'], 0)
    
    def test_output_structure_consistency(self):
        """Test that all required output fields are present and properly typed"""
        test_params = {
            "Acceptable monthly payment": [self.acceptable_payment],
            "Investment interest rate": [self.investment_rate],
            "Expected inflation": [self.inflation_rate]
        }
        results = calculate_credit_with_investment(self.credit_results, test_params)
        
        # Verify all required fields are present and properly typed
        for years, data in results.items():
            self.assertIn('monthly_payment', data)
            self.assertIn('total_cost', data)
            self.assertIn('total_cost_adjusted', data)
            self.assertIn('investment_balance', data)
            self.assertIsInstance(data['monthly_payment'], (int, float))
            self.assertIsInstance(data['total_cost'], (int, float))
            self.assertIsInstance(data['total_cost_adjusted'], (int, float))
            self.assertIsInstance(data['investment_balance'], (int, float))


if __name__ == '__main__':
    unittest.main()