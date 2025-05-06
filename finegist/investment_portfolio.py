class InvestmentPortfolio:
    def __init__(self):
        """
            Initialize the investment portfolio with an empty list of investments.
        """

        self.investments = []

    def add_investment(self, name, amount, current_value):
        """
            Add an investment to the portfolio.
            :param name: Name of the investment.
            :param amount : Amount invested.
            :param current_value : Current value of the investment.
        """

        if amount <= 0 or current_value <= 0:
            raise ValueError("Amount must be greater than zero and current value must be non - negative.")
        self.investments.append({"name" : name, "amount" : amount, "current_value" : current_value})

    def total_invested(self):
        """
            Calculate the total current value of all investments.
        """

        return sum(investment["amount"] for investment in self.investments)

    def total_current_value(self):
        """
        Calculate the total current value of all investments.
        """

        return sum(investment["current_value"] for investment in self.investments)

    def portfolio_summary(self):
        """
        Return a summary of the portfolio.
        """

        return {
            "total_invested": self.total_invested(),
            "total_current_value": self.total_current_value(),
            "investments": self.investments,
        }