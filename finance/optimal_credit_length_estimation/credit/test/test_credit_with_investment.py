import unittest
from credit.credit_with_investment import calculate_credit_with_investment
from credit.simple_credit import calculate_credit


class TestCreditWithInvestment(unittest.TestCase):
    
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


if __name__ == '__main__':
    unittest.main()