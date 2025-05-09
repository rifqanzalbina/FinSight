from datetime import datetime, timedelta

class FinancialGoalPlanner:
    def __init__(self, goal_name, )
        """
            Initialize the financial goal planner with an empty list of goals 
        """

        self.goals = []

    def add_goal(self, name, target_amount, start_date, end_date):
        """
            Add a financial goal to the planner.
            :param name : Name or description of the goal.
            :param target_amount : The target amountt to reach.
            :param current_amount : The current amount saved (default 0).
            :param monthly_contribution : The monthly contribution towards the goal (default 0)
        """

        if target_amount <= 0:
            raise ValueError("Target amount must be greater than zero.")
        if current_amount < 0:
            raise ValueError("Current amount must be non-negative.")
        if monthly_contribution < 0:
            raise ValueError("Monthly contribution must be non-negative.")

        self.goals.append({
            "name" : name,
            "target_amount" : target_amount,
            "current_amount" : current_amount,
            "monthly_contribution" : monthly_contribution,
            "creation_date" : datetime.now(),
        })
        return len(self.goals) - 1 # Return the index of the added goal
    
    def update_goal(self, index, current_amount=None, monthly_contribution = None):
        """
            Update a goal's current amount or monthly contribution.
            :param index : The index of the goal to update.
            :param current_amount : The new current amount(optional).
            :param monthly_contribution : The new monthly contribution (optional).
        """

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


    def calculate_prgress(self, index):
        """
            Calculate the progress towards a goal as a percentage.
            :param index: The index of the goal.
            :return: the progress as a percentage.
        """
        if index < 0 or index >= len(self.goals):
            raise ValueError("Invalid goal index.")

        goal = self.goals[index]
        return (goal["current_amount"] / goal["target_amount"]) * 100

    def estimate_completion_time(self, index):
        """
            Estimate the time required to reach a goal based on the current amount and monthly contribution.
            :param index: The index of the goal.
            :return: The estimated completion time in months or None if it can't be estimated.
        """

        









    




    