import unittest
from datetime import datetime, timedelta
from finegist.financial_goal_planner import FinancialGoalPlanner

class TestFinancialGoalPlanner(unittest.TestCase):
    def setUp(self):
        """
        Set up an instance of FinancialGoalPlanner for testing.
        """
        self.planner = FinancialGoalPlanner()

    def test_add_goal(self):
        """
        Test adding a financial goal to the planner.
        """
        goal_index = self.planner.add_goal("Buy a House", 500000, 50000, 2000)
        self.assertEqual(goal_index, 0)
        self.assertEqual(len(self.planner.goals), 1)
        self.assertEqual(self.planner.goals[0]["name"], "Buy a House")
        self.assertEqual(self.planner.goals[0]["target_amount"], 500000)
        self.assertEqual(self.planner.goals[0]["current_amount"], 50000)
        self.assertEqual(self.planner.goals[0]["monthly_contribution"], 2000)

    def test_invalid_target_amount(self):
        """
        Test adding a goal with an invalid target amount.
        """
        with self.assertRaises(ValueError):
            self.planner.add_goal("Invalid Goal", -500000, 50000, 2000)

    def test_invalid_current_amount(self):
        """
        Test adding a goal with an invalid current amount.
        """
        with self.assertRaises(ValueError):
            self.planner.add_goal("Invalid Goal", 500000, -50000, 2000)

    def test_invalid_monthly_contribution(self):
        """
        Test adding a goal with an invalid monthly contribution.
        """
        with self.assertRaises(ValueError):
            self.planner.add_goal("Invalid Goal", 500000, 50000, -2000)

    def test_update_goal(self):
        """
        Test updating a goal's information.
        """
        goal_index = self.planner.add_goal("Buy a House", 500000, 50000, 2000)
        self.planner.update_goal(goal_index, current_amount=60000, monthly_contribution=2500)
        self.assertEqual(self.planner.goals[goal_index]["current_amount"], 60000)
        self.assertEqual(self.planner.goals[goal_index]["monthly_contribution"], 2500)

    def test_calculate_progress(self):
        """
        Test calculating the progress towards a goal.
        """
        goal_index = self.planner.add_goal("Buy a House", 500000, 50000, 2000)
        progress = self.planner.calculate_progress(goal_index)
        self.assertEqual(progress, 10.0)  # 50,000 / 500,000 * 100 = 10%

    def test_estimate_completion_time(self):
        """
        Test estimating the completion time for a goal.
        """
        goal_index = self.planner.add_goal("Buy a House", 500000, 50000, 2000)
        months = self.planner.estimate_completion_time(goal_index)
        self.assertEqual(months, 225.0)  # (500,000 - 50,000) / 2,000 = 225 months

    def test_goal_already_reached(self):
        """
        Test completion time for a goal that has already been reached.
        """
        goal_index = self.planner.add_goal("Small Goal", 1000, 1000, 100)
        months = self.planner.estimate_completion_time(goal_index)
        self.assertEqual(months, 0)  # Goal already reached

    def test_calculate_expected_completion_date(self):
        """
        Test calculating the expected completion date of a goal.
        """
        goal_index = self.planner.add_goal("Buy a House", 500000, 50000, 2000)
        expected_date = self.planner.calculate_expected_completion_date(goal_index)
        creation_date = self.planner.goals[goal_index]["creation_date"]
        expected_calculation = creation_date + timedelta(days=30 * 225)
        
        # Compare year, month and day, not exact time
        self.assertEqual(expected_date.year, expected_calculation.year)
        self.assertEqual(expected_date.month, expected_calculation.month)
        self.assertEqual(expected_date.day, expected_calculation.day)

if __name__ == "__main__":
    unittest.main()