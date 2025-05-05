class Budget : 
    def __init__(self, name, total_amount):
        """
            Initialize a budget with a name and total amount.
        """

        self.name = name
        self.total_amount = total_amount
        self.expenses = []

    def add_expense(self, description, amount):
        """
            Add an expense to the budget.
        """

        if amount > self.total_amount : 
            raise ValueError("Expense exceeds remaining budget.")
        self.expenses.append({"description" : description, "amount" : amount})

    def total_expenses(self):
        """
            Calculate the total expenses.
        """
        return sum(expense["amount"] for expense in self.expenses)

    def remaining_budget(self):
        """
            Caclulate the remaining budget.
        """

        return self.total_amount - self.total_expenses()

    def summary(self):
        """
            Return a summary of the budget.
        """

        return {
            "name" : self.name,
            "total_amount" : self.total_amount,
            "total_expenses" : self.total_expenses(),
            "remaining_budget" : self.remaining_budget(),
        }