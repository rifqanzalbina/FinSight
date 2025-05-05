from finegist.budget import Budget

# Create a budget
my_budget = Budget("Monthly Budget", 5000)

# Add expenses
my_budget.add_expense("Groceries", 1500)
my_budget.add_expense("Rent", 2000)

# Print summary
print(my_budget.summary())