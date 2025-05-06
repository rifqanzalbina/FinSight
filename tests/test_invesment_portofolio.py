import unittest
from finegist.investment_portfolio import InvestmentPortfolio

class TestInvestmentPortfolio(unittest.TestCase):
    def setUp(self):
        """
        Set up an instance of InvestmentPortfolio for testing.
        """
        self.portfolio = InvestmentPortfolio()

    def test_add_investment(self):
        """
        Test adding an investment to the portfolio.
        """
        self.portfolio.add_investment("Stock A", 1000, 1200)
        self.assertEqual(len(self.portfolio.investments), 1)
        self.assertEqual(self.portfolio.investments[0]["name"], "Stock A")
        self.assertEqual(self.portfolio.investments[0]["amount"], 1000)
        self.assertEqual(self.portfolio.investments[0]["current_value"], 1200)

    def test_add_investment_invalid_values(self):
        """
        Test adding an investment with invalid values.
        """
        with self.assertRaises(ValueError):
            self.portfolio.add_investment("Stock B", -500, 1000)
        with self.assertRaises(ValueError):
            self.portfolio.add_investment("Stock C", 500, -100)

    def test_total_invested(self):
        """
        Test calculating the total amount invested.
        """
        self.portfolio.add_investment("Stock A", 1000, 1200)
        self.portfolio.add_investment("Stock B", 2000, 2500)
        self.assertEqual(self.portfolio.total_invested(), 3000)

    def test_total_current_value(self):
        """
        Test calculating the total current value of investments.
        """
        self.portfolio.add_investment("Stock A", 1000, 1200)
        self.portfolio.add_investment("Stock B", 2000, 2500)
        self.assertEqual(self.portfolio.total_current_value(), 3700)

    def test_portfolio_summary(self):
        """
        Test generating a summary of the portfolio.
        """
        self.portfolio.add_investment("Stock A", 1000, 1200)
        self.portfolio.add_investment("Stock B", 2000, 2500)
        summary = self.portfolio.portfolio_summary()
        self.assertEqual(summary["total_invested"], 3000)
        self.assertEqual(summary["total_current_value"], 3700)
        self.assertEqual(len(summary["investments"]), 2)

if __name__ == "__main__":
    unittest.main()