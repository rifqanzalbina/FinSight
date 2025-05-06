import unittest
from finegist.savings_calculator import SavingsCalculator

class TestSavingsCalculator(unittest.TestCase):
    def setUp(self):
        """
        Set up an instance of SavingsCalculator for testing.
        """
        self.calculator = SavingsCalculator(income=5000, expenses=3000)

    def test_calculate_savings(self):
        """
        Test calculating monthly savings.
        """
        self.assertEqual(self.calculator.calculate_savings(), 2000)

    def test_calculate_months_to_target(self):
        """
        Test calculating months to reach a target savings.
        """
        self.assertEqual(self.calculator.calculate_months_to_target(10000), 5)

    def test_negative_income(self):
        """
        Test initializing with negative income.
        """
        with self.assertRaises(ValueError):
            SavingsCalculator(income=-5000, expenses=3000)

    def test_negative_expenses(self):
        """
        Test initializing with negative expenses.
        """
        with self.assertRaises(ValueError):
            SavingsCalculator(income=5000, expenses=-3000)

    def test_negative_target_savings(self):
        """
        Test calculating months to a negative target savings.
        """
        with self.assertRaises(ValueError):
            self.calculator.calculate_months_to_target(-10000)

    def test_zero_monthly_savings(self):
        """
        Test calculating months to target when monthly savings are zero.
        """
        calculator = SavingsCalculator(income=3000, expenses=3000)
        with self.assertRaises(ValueError):
            calculator.calculate_months_to_target(10000)

if __name__ == "__main__":
    unittest.main()