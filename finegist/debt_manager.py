class DebtManager:
    def __init__(self):
        """
        Initialize the debt manager with an empty list of debts.
        """
        self.debts = []
        self.additional_payment = 0
        
    def add_debt(self, name, balance, interest_rate, minimum_payment):
        """
        Add a debt to be managed.
        :param name: Name/description of the debt
        :param balance: Current outstanding balance
        :param interest_rate: Annual interest rate (as percentage, e.g. 5 for 5%)
        :param minimum_payment: Minimum monthly payment required
        """
        if balance <= 0:
            raise ValueError("Balance must be greater than zero")
        if interest_rate < 0:
            raise ValueError("Interest rate cannot be negative")
        if minimum_payment <= 0:
            raise ValueError("Minimum payment must be greater than zero")
        
        debt = {
            "name": name,
            "balance": balance,
            "interest_rate": interest_rate / 100.0,  # Convert to decimal
            "minimum_payment": minimum_payment,
            "original_balance": balance
        }
        self.debts.append(debt)
        return len(self.debts) - 1  # Return the index of the added debt
        
    def set_additional_payment(self, amount):
        """
        Set an additional monthly payment to be applied based on the chosen strategy.
        :param amount: Additional monthly payment amount
        """
        if amount < 0:
            raise ValueError("Additional payment cannot be negative")
        self.additional_payment = amount
        
    def total_debt(self):
        """
        Calculate the total outstanding debt.
        :return: Sum of all debt balances
        """
        return sum(debt["balance"] for debt in self.debts)
    
    def total_minimum_payment(self):
        """
        Calculate the total minimum payment required for all debts.
        :return: Sum of all minimum payments
        """
        return sum(debt["minimum_payment"] for debt in self.debts)
    
    def _apply_interest_and_minimum_payments(self, debts):
        """
        Apply monthly interest and minimum payments to debts.
        :param debts: List of debt dictionaries
        :return: Updated list of debts and total minimum payment applied
        """
        total_payment_applied = 0
        for debt in debts:
            if debt["balance"] <= 0:
                continue
                
            # Apply interest (monthly interest = annual interest / 12)
            monthly_interest = debt["balance"] * (debt["interest_rate"] / 12)
            debt["balance"] += monthly_interest
            
            # Apply minimum payment
            payment = min(debt["balance"], debt["minimum_payment"])
            debt["balance"] -= payment
            total_payment_applied += payment
            
        return debts, total_payment_applied
    
    def _apply_additional_payment(self, debts, additional_payment, strategy="avalanche"):
        """
        Apply additional payment to debts based on selected strategy.
        :param debts: List of debt dictionaries
        :param additional_payment: Additional amount to pay
        :param strategy: 'avalanche' (highest interest first) or 'snowball' (lowest balance first)
        :return: Updated list of debts
        """
        if additional_payment <= 0 or all(debt["balance"] <= 0 for debt in debts):
            return debts
        
        # Sort debts based on strategy
        active_debts = [d for d in debts if d["balance"] > 0]
        if len(active_debts) == 0:
            return debts
            
        if strategy == "avalanche":
            # Sort by highest interest rate
            target_index = max(range(len(active_debts)), 
                              key=lambda i: active_debts[i]["interest_rate"])
        else:  # "snowball"
            # Sort by lowest balance
            target_index = min(range(len(active_debts)), 
                              key=lambda i: active_debts[i]["balance"])
        
        # Find the actual index in the original debts list
        original_index = debts.index(active_debts[target_index])
        
        # Apply additional payment to the target debt
        payment = min(debts[original_index]["balance"], additional_payment)
        debts[original_index]["balance"] -= payment
        
        return debts
    
    def generate_payment_plan(self, strategy="avalanche", max_months=360):
        """
        Generate a debt payment plan based on the chosen strategy.
        :param strategy: 'avalanche' (highest interest first) or 'snowball' (lowest balance first)
        :param max_months: Maximum number of months to simulate (default 30 years)
        :return: Payment plan details
        """
        if not self.debts:
            raise ValueError("No debts have been added")
        
        if strategy not in ["avalanche", "snowball"]:
            raise ValueError("Strategy must be either 'avalanche' or 'snowball'")
        
        # Create a deep copy of debts to avoid modifying the originals
        debts = [{k: v for k, v in debt.items()} for debt in self.debts]
        
        payment_plan = []
        month = 0
        total_interest_paid = 0
        total_paid = 0
        
        while any(debt["balance"] > 0 for debt in debts) and month < max_months:
            month += 1
            
            # Track starting balances for interest calculation
            starting_balances = {i: debt["balance"] for i, debt in enumerate(debts)}
            
            # Apply interest and minimum payments
            debts, minimum_payment_applied = self._apply_interest_and_minimum_payments(debts)
            
            # Apply additional payment based on strategy
            debts = self._apply_additional_payment(debts, self.additional_payment, strategy)
            
            # Calculate interest paid this month
            interest_paid = sum(
                debt["balance"] - (starting_balances[i] - debt["minimum_payment"]) 
                for i, debt in enumerate(debts)
                if starting_balances[i] > 0
            )
            
            # Keep interest positive even if it's the last payment that's less than the minimum
            interest_paid = max(0, interest_paid)
            total_interest_paid += interest_paid
            
            # Calculate total paid this month
            month_payment = minimum_payment_applied + self.additional_payment
            if month_payment > sum(starting_balances.values()):
                month_payment = sum(starting_balances.values())
            
            total_paid += month_payment
            
            # Record month's details
            month_data = {
                "month": month,
                "total_balance": sum(debt["balance"] for debt in debts),
                "interest_paid": interest_paid,
                "payment_amount": month_payment,
                "debts": [{
                    "name": debt["name"],
                    "balance": debt["balance"],
                    "paid_this_month": starting_balances[i] - debt["balance"]
                } for i, debt in enumerate(debts)]
            }
            payment_plan.append(month_data)
        
        result = {
            "strategy": strategy,
            "months_to_payoff": month,
            "total_interest_paid": total_interest_paid,
            "total_paid": total_paid,
            "original_debt": sum(debt["original_balance"] for debt in debts),
            "payment_plan": payment_plan,
            "paid_off_successfully": month < max_months
        }
        
        return result
    
    def compare_strategies(self, max_months=360):
        """
        Compare snowball and avalanche strategies.
        :param max_months: Maximum number of months to simulate
        :return: Dictionary comparing both strategies
        """
        snowball_plan = self.generate_payment_plan("snowball", max_months)
        avalanche_plan = self.generate_payment_plan("avalanche", max_months)
        
        comparison = {
            "snowball_months": snowball_plan["months_to_payoff"],
            "avalanche_months": avalanche_plan["months_to_payoff"],
            "snowball_interest": snowball_plan["total_interest_paid"],
            "avalanche_interest": avalanche_plan["total_interest_paid"],
            "difference_months": snowball_plan["months_to_payoff"] - avalanche_plan["months_to_payoff"],
            "difference_interest": snowball_plan["total_interest_paid"] - avalanche_plan["total_interest_paid"],
            "optimal_strategy": "avalanche" if avalanche_plan["total_interest_paid"] <= snowball_plan["total_interest_paid"] else "snowball"
        }
        
        return comparison
    
    def amortization_schedule(self, debt_index, extra_payment=0):
        """
        Generate an amortization schedule for a specific debt.
        :param debt_index: Index of the debt
        :param extra_payment: Optional extra payment to apply monthly
        :return: List of monthly payment details
        """
        if debt_index < 0 or debt_index >= len(self.debts):
            raise ValueError("Invalid debt index")
            
        debt = {k: v for k, v in self.debts[debt_index].items()}  # Create a copy
        
        schedule = []
        month = 0
        total_interest = 0
        
        while debt["balance"] > 0 and month < 360:  # 30 years max
            month += 1
            
            # Calculate interest for this month
            interest = debt["balance"] * (debt["interest_rate"] / 12)
            total_interest += interest
            
            # Add interest to balance
            debt["balance"] += interest
            
            # Calculate payment
            payment = debt["minimum_payment"] + extra_payment
            payment = min(payment, debt["balance"])  # Don't pay more than remaining balance
            
            # Apply payment
            debt["balance"] -= payment
            
            # Record details
            schedule.append({
                "month": month,
                "payment": payment,
                "principal": payment - interest,
                "interest": interest,
                "remaining_balance": debt["balance"],
                "total_interest_paid": total_interest
            })
            
        return schedule