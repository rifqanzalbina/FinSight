class SavingsCalculator:
    def __init__(self, income, expenses):
        """
        Initialize the savings calculator with income and expenses.
        :param income: Total monthly income.
        :param expenses: Total monthly expenses.
        """
        if income < 0:
            raise ValueError("Income must be non-negative.")
        if expenses < 0:
            raise ValueError("Expenses must be non-negative.")
        self.income = income
        self.expenses = expenses

    def calculate_savings(self):
        """
        Calculate the monthly savings.
        """
        return self.income - self.expenses

    def calculate_months_to_target(self, target_savings):
        """
        Calculate the number of months required to reach a target savings.
        :param target_savings: The target savings amount.
        """
        if target_savings < 0:
            raise ValueError("Target savings must be non-negative.")
        monthly_savings = self.calculate_savings()
        if monthly_savings <= 0:
            raise ValueError("Monthly savings must be greater than zero to reach the target.")
        return target_savings / monthly_savings