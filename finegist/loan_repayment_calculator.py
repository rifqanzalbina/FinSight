class LoanRepaymentCalculator:
    def __init__(self, principal, annual_interest_rate, years):
        """
        Initialize the loan repayment calculator.
        :param principal: The total loan amount.
        :param annual_interest_rate: The annual interest rate (in percentage).
        :param years: The loan duration in years.
        """
        if principal <= 0:
            raise ValueError("Principal must be greater than zero.")
        if annual_interest_rate < 0:
            raise ValueError("Annual interest rate must be non-negative.")
        if years <= 0:
            raise ValueError("Loan duration must be greater than zero.")

        self.principal = principal
        self.annual_interest_rate = annual_interest_rate / 100  # Convert to decimal
        self.years = years

    def calculate_monthly_payment(self):
        """
        Calculate the fixed monthly payment using the loan formula.
        """
        monthly_interest_rate = self.annual_interest_rate / 12
        total_payments = self.years * 12

        if monthly_interest_rate == 0:  # No interest case
            return self.principal / total_payments

        # Loan payment formula
        monthly_payment = (
            self.principal
            * monthly_interest_rate
            * (1 + monthly_interest_rate) ** total_payments
        ) / ((1 + monthly_interest_rate) ** total_payments - 1)

        return monthly_payment

    def generate_repayment_schedule(self):
        """
        Generate the repayment schedule showing principal and interest breakdown.
        """
        monthly_payment = self.calculate_monthly_payment()
        monthly_interest_rate = self.annual_interest_rate / 12
        remaining_balance = self.principal
        schedule = []

        for month in range(1, self.years * 12 + 1):
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment

            schedule.append({
                "month": month,
                "principal_payment": round(principal_payment, 2),
                "interest_payment": round(interest_payment, 2),
                "remaining_balance": round(remaining_balance, 2),
            })

        return schedule