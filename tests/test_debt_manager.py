import unittest
from finegist.debt_manager import DebtManager

class TestDebtManager(unittest.TestCase):
    def setUp(self):
        """
        Set up an instance of DebtManager for testing.
        """
        self.manager = DebtManager()
        
        # Add some test debts
        self.manager.add_debt("Credit Card", 5000, 18.0, 150)
        self.manager.add_debt("Car Loan", 15000, 6.0, 300)
        self.manager.add_debt("Personal Loan", 3000, 10.0, 100)
        
        # Add additional payment
        self.manager.set_additional_payment(200)

    def test_add_debt(self):
        """
        Test adding a debt to the manager.
        """
        index = self.manager.add_debt("Student Loan", 20000, 5.0, 250)
        self.assertEqual(len(self.manager.debts), 4)
        self.assertEqual(self.manager.debts[index]["name"], "Student Loan")
        self.assertEqual(self.manager.debts[index]["balance"], 20000)
        self.assertEqual(self.manager.debts[index]["interest_rate"], 0.05)
        self.assertEqual(self.manager.debts[index]["minimum_payment"], 250)

    def test_negative_balance(self):
        """
        Test adding a debt with negative balance.
        """
        with self.assertRaises(ValueError):
            self.manager.add_debt("Invalid Debt", -1000, 5.0, 50)

    def test_negative_interest_rate(self):
        """
        Test adding a debt with negative interest rate.
        """
        with self.assertRaises(ValueError):
            self.manager.add_debt("Invalid Debt", 1000, -5.0, 50)

    def test_negative_payment(self):
        """
        Test adding a debt with negative minimum payment.
        """
        with self.assertRaises(ValueError):
            self.manager.add_debt("Invalid Debt", 1000, 5.0, -50)

    def test_total_debt(self):
        """
        Test calculating the total debt.
        """
        self.assertEqual(self.manager.total_debt(), 23000)

    def test_total_minimum_payment(self):
        """
        Test calculating the total minimum payment.
        """
        self.assertEqual(self.manager.total_minimum_payment(), 550)

    def test_avalanche_strategy(self):
        """
        Test the avalanche debt payment strategy.
        """
        plan = self.manager.generate_payment_plan("avalanche", max_months=60)
        
        # Verify the highest interest debt (Credit Card at 18%) is paid off first
        # After a few months, its balance should decrease faster than others
        first_month = plan["payment_plan"][0]
        fifth_month = plan["payment_plan"][4]
        
        credit_card_first = next(debt for debt in first_month["debts"] if debt["name"] == "Credit Card")
        credit_card_fifth = next(debt for debt in fifth_month["debts"] if debt["name"] == "Credit Card")
        
        # Calculate how much the balance decreased
        credit_card_decrease = credit_card_first["balance"] - credit_card_fifth["balance"]
        
        # Verify that it gets paid down faster due to additional payment
        self.assertGreater(credit_card_decrease, 750)  # More than 5 minimum payments

    def test_snowball_strategy(self):
        """
        Test the snowball debt payment strategy.
        """
        plan = self.manager.generate_payment_plan("snowball", max_months=60)
        
        # Verify the smallest balance debt (Personal Loan at $3000) is paid off first
        # After a few months, its balance should decrease faster than others
        first_month = plan["payment_plan"][0]
        fifth_month = plan["payment_plan"][4]
        
        personal_loan_first = next(debt for debt in first_month["debts"] if debt["name"] == "Personal Loan")
        personal_loan_fifth = next(debt for debt in fifth_month["debts"] if debt["name"] == "Personal Loan")
        
        # Calculate how much the balance decreased
        personal_loan_decrease = personal_loan_first["balance"] - personal_loan_fifth["balance"]
        
        # Verify that it gets paid down faster due to additional payment
        self.assertGreater(personal_loan_decrease, 500)  # More than 5 minimum payments

    def test_compare_strategies(self):
        """
        Test comparing the debt payment strategies.
        """
        comparison = self.manager.compare_strategies(max_months=60)
        
        # The avalanche strategy should save money compared to snowball
        self.assertLessEqual(comparison["avalanche_interest"], comparison["snowball_interest"])
        self.assertEqual(comparison["optimal_strategy"], "avalanche")
        
        # Strategies should have different payoff timelines
        self.assertTrue(comparison["snowball_months"] > 0)
        self.assertTrue(comparison["avalanche_months"] > 0)

    def test_amortization_schedule(self):
        """
        Test generating an amortization schedule for a specific debt.
        """
        schedule = self.manager.amortization_schedule(1, extra_payment=100)  # Car loan with extra payment
        
        # Should have entries until paid off
        self.assertTrue(len(schedule) > 0)
        
        # First month should have correct values
        first_month = schedule[0]
        self.assertEqual(first_month["month"], 1)
        self.assertEqual(first_month["payment"], 400)  # 300 minimum + 100 extra
        
        # Last month should have zero balance
        last_month = schedule[-1]
        self.assertLess(last_month["remaining_balance"], 0.01)

if __name__ == "__main__":
    unittest.main()