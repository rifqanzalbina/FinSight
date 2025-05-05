import unittest
from finegist.budget import Budget

class TestBudget(unittest.TestCase):
    def setUp(self):  # Perbaikan: Ubah "setup" menjadi "setUp"
        """
        Set up a budget instance for testing.
        """
        self.budget = Budget("Test Budget", 5000)

    def test_initial_budget(self):
        """
        Test the initial state of the budget.
        """
        self.assertEqual(self.budget.name, "Test Budget")
        self.assertEqual(self.budget.total_amount, 5000)
        self.assertEqual(self.budget.total_expenses(), 0)
        self.assertEqual(self.budget.remaining_budget(), 5000)

    def test_add_expense(self):
        """
        Test adding an expense to the budget.
        """
        self.budget.add_expense("Groceries", 1500)
        self.assertEqual(self.budget.total_expenses(), 1500)
        self.assertEqual(self.budget.remaining_budget(), 3500)  # Perbaikan: Ubah 35000 menjadi 3500

    def test_add_expense_exceeding_budget(self):
        """
        Test adding an expense that exceeds the remaining budget.
        """
        with self.assertRaises(ValueError):
            self.budget.add_expense("Luxury Item", 6000)

    def test_summary(self):
        """
        Test the summary of the budget.
        """
        self.budget.add_expense("Groceries", 1500)
        self.budget.add_expense("Rent", 2000)
        summary = self.budget.summary()
        self.assertEqual(summary["name"], "Test Budget")
        self.assertEqual(summary["total_amount"], 5000)
        self.assertEqual(summary["total_expenses"], 3500)
        self.assertEqual(summary["remaining_budget"], 1500)

if __name__ == "__main__":
    unittest.main()