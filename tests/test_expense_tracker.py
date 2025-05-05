import unittest
from datetime import datetime, timedelta
from finegist.expense_tracker import ExpenseTracker

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        """
        Set up an instance of ExpenseTracker for testing.
        """
        self.tracker = ExpenseTracker()

    def test_add_expense(self):
        """
        Test adding an expense to the tracker.
        """
        self.tracker.add_expense("Lunch", 50)
        self.assertEqual(len(self.tracker.expenses), 1)
        self.assertEqual(self.tracker.expenses[0]["description"], "Lunch")
        self.assertEqual(self.tracker.expenses[0]["amount"], 50)

    def test_add_expense_with_date(self):
        """
        Test adding an expense with a specific date.
        """
        date = datetime(2025, 5, 1).date()
        self.tracker.add_expense("Dinner", 100, date)
        self.assertEqual(self.tracker.expenses[0]["date"], date)

    def test_add_expense_invalid_amount(self):
        """
        Test adding an expense with an invalid amount.
        """
        with self.assertRaises(ValueError):
            self.tracker.add_expense("Invalid Expense", -10)

    def test_total_expenses(self):
        """
        Test calculating the total expenses.
        """
        self.tracker.add_expense("Lunch", 50)
        self.tracker.add_expense("Dinner", 100)
        self.assertEqual(self.tracker.total_expenses(), 150)

    def test_expenses_by_date(self):
        """
        Test filtering expenses by date.
        """
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        self.tracker.add_expense("Lunch", 50, today)
        self.tracker.add_expense("Dinner", 100, yesterday)
        today_expenses = self.tracker.expenses_by_date(today)
        self.assertEqual(len(today_expenses), 1)
        self.assertEqual(today_expenses[0]["description"], "Lunch")

    def test_summary(self):
        """
        Test generating a summary of expenses grouped by date.
        """
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        self.tracker.add_expense("Lunch", 50, today)
        self.tracker.add_expense("Dinner", 100, yesterday)
        summary = self.tracker.summary()
        self.assertEqual(summary[today], 50)
        self.assertEqual(summary[yesterday], 100)

if __name__ == "__main__":
    unittest.main()