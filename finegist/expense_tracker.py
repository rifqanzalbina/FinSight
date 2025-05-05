from datetime import datetime

class ExpenseTracker:
    def __init__(self):
        """
        Initialize the expense tracker with an empty list of expenses.
        """
        self.expenses = []

    def add_expense(self, description, amount, date=None):
        """
        Add an expense to the tracker.
        :param description: Description of the expense.
        :param amount: Amount of the expense.
        :param date: Date of the expense (optional, defaults to today).
        """
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if date is None:
            date = datetime.now().date()
        self.expenses.append({"description": description, "amount": amount, "date": date})

    def total_expenses(self):
        """
        Calculate the total amount of all expenses.
        """
        return sum(expense["amount"] for expense in self.expenses)

    def expenses_by_date(self, date):
        """
        Get all expenses for a specific date.
        :param date: The date to filter expenses by.
        """
        return [expense for expense in self.expenses if expense["date"] == date]

    def summary(self):
        """
        Return a summary of all expenses grouped by date.
        """
        summary = {}
        for expense in self.expenses:
            date = expense["date"]
            if date not in summary:
                summary[date] = 0
            summary[date] += expense["amount"]
        return summary