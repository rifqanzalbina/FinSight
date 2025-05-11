from datetime import datetime, timedelta

class FinancialGoalPlanner:
    def __init__(self):
        """
        Initialize the financial goal planner with an empty list of goals.
        """
        self.goals = []

    def add_goal(self, name, target_amount, current_amount=0, monthly_contribution=0):
        """
        Add a financial goal to the planner.
        :param name: Name or description of the goal.
        :param target_amount: The target amount to reach.
        :param current_amount: The current amount saved (default 0).
        :param monthly_contribution: The monthly contribution towards the goal (default 0).
        """
        if target_amount <= 0:
            raise ValueError("Target amount must be greater than zero.")
        if current_amount < 0:
            raise ValueError("Current amount must be non-negative.")
        if monthly_contribution < 0:
            raise ValueError("Monthly contribution must be non-negative.")

        self.goals.append({
            "name": name,
            "target_amount": target_amount,
            "current_amount": current_amount,
            "monthly_contribution": monthly_contribution,
            "creation_date": datetime.now()
        })
        return len(self.goals) - 1  # Return the index of the added goal

    def update_goal(self, index, current_amount=None, monthly_contribution=None):
        """
        Update a goal's current amount or monthly contribution.
        :param index: The index of the goal to update.
        :param current_amount: The new current amount (optional).
        :param monthly_contribution: The new monthly contribution (optional).
        """
        first_value = 20
        if index < 0 or index >= len(self.goals):
            raise ValueError("Invalid goal index.")

        if current_amount is not None:
            if current_amount < 0:
                raise ValueError("Current amount must be non-negative.")
            self.goals[index]["current_amount"] = current_amount

        if monthly_contribution is not None:
            if monthly_contribution < 0:
                raise ValueError("Monthly contribution must be non-negative.")
            self.goals[index]["monthly_contribution"] = monthly_contribution

    def calculate_progress(self, index):
        """
        Calculate the progress towards a goal as a percentage.
        :param index: The index of the goal.
        :return: The progress as a percentage.
        """
        if index < 0 or index >= len(self.goals):
            raise ValueError("Invalid goal index.")
            
        goal = self.goals[index]
        return (goal["current_amount"] / goal["target_amount"]) * 100

    def estimate_completion_time(self, index):
        """
        Estimate the time to complete a goal based on the monthly contribution.
        :param index: The index of the goal.
        :return: The estimated completion time in months or None if it can't be estimated.
        """
        if index < 0 or index >= len(self.goals):
            raise ValueError("Invalid goal index.")

        goal = self.goals[index]
        remaining_amount = goal["target_amount"] - goal["current_amount"]
        
        if remaining_amount <= 0:
            return 0  # Goal already reached
            
        if goal["monthly_contribution"] <= 0:
            return None  # Can't estimate without monthly contribution
            
        months = remaining_amount / goal["monthly_contribution"]
        return months

    def calculate_expected_completion_date(self, index):
        """
        Calculate the expected completion date of a goal.
        :param index: The index of the goal.
        :return: The expected completion date or None if it can't be calculated.
        """
        months = self.estimate_completion_time(index)
        if months is None:
            return None
            
        goal = self.goals[index]
        return goal["creation_date"] + timedelta(days=30 * months) 