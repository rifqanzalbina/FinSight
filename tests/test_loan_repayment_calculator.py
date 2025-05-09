import unittest
from finegist.loan_repayment_calculator import LoanRepaymentCalculator

class TestLoanRepaymentCalculator(unittest.TestCase):
    def setUp(self):
        """
        Set up an instance of LoanRepaymentCalculator for testing.
        """
        self.calculator = LoanRepaymentCalculator(principal=100000, annual_interest_rate=5, years=10)

    def test_calculate_monthly_payment(self):
        """
        Test calculating the monthly payment.
        """
        monthly_payment = self.calculator.calculate_monthly_payment()
        self.assertAlmostEqual(monthly_payment, 1060.66, places=2)

    def test_generate_repayment_schedule(self):
        """
        Test generating the repayment schedule.
        """
        schedule = self.calculator.generate_repayment_schedule()
        self.assertEqual(len(schedule), 120)  # 10 years * 12 months
        self.assertAlmostEqual(schedule[0]["principal_payment"] + schedule[0]["interest_payment"], 1060.66, places=2)
        self.assertAlmostEqual(schedule[-1]["remaining_balance"], 0, places=2)

    def test_invalid_principal(self):
        """
        Test initializing with an invalid principal amount.
        """
        with self.assertRaises(ValueError):
            LoanRepaymentCalculator(principal=-100000, annual_interest_rate=5, years=10)

    def test_invalid_interest_rate(self):
        """
        Test initializing with an invalid interest rate.
        """
        with self.assertRaises(ValueError):
            LoanRepaymentCalculator(principal=100000, annual_interest_rate=-5, years=10)

    def test_invalid_years(self):
        """
        Test initializing with an invalid loan duration.
        """
        with self.assertRaises(ValueError):
            LoanRepaymentCalculator(principal=100000, annual_interest_rate=5, years=0)

if __name__ == "__main__":
    unittest.main()