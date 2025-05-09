import unittest
from finegist.net_worth_calculator import NetWorthCalculator

class TestNetWorthCalculator(unittest.TestCase):
    def setUp(self):
        """
        Set up an instance of NetWorthCalculator for testing.
        """
        self.calculator = NetWorthCalculator()

    def test_add_asset(self):
        """
        Test adding an asset to the calculator.
        """
        self.calculator.add_asset("House", 500000)
        self.assertEqual(len(self.calculator.assets), 1)
        self.assertEqual(self.calculator.assets[0]["name"], "House")
        self.assertEqual(self.calculator.assets[0]["value"], 500000)

    def test_add_liability(self):
        """
        Test adding a liability to the calculator.
        """
        self.calculator.add_liability("Mortgage", 200000)
        self.assertEqual(len(self.calculator.liabilities), 1)
        self.assertEqual(self.calculator.liabilities[0]["name"], "Mortgage")
        self.assertEqual(self.calculator.liabilities[0]["value"], 200000)

    def test_total_assets(self):
        """
        Test calculating the total value of assets.
        """
        self.calculator.add_asset("House", 500000)
        self.calculator.add_asset("Car", 30000)
        self.assertEqual(self.calculator.total_assets(), 530000)

    def test_total_liabilities(self):
        """
        Test calculating the total value of liabilities.
        """
        self.calculator.add_liability("Mortgage", 200000)
        self.calculator.add_liability("Car Loan", 15000)
        self.assertEqual(self.calculator.total_liabilities(), 215000)

    def test_calculate_net_worth(self):
        """
        Test calculating the net worth.
        """
        self.calculator.add_asset("House", 500000)
        self.calculator.add_asset("Car", 30000)
        self.calculator.add_liability("Mortgage", 200000)
        self.calculator.add_liability("Car Loan", 15000)
        self.assertEqual(self.calculator.calculate_net_worth(), 315000)

    def test_negative_asset_value(self):
        """
        Test adding an asset with a negative value.
        """
        with self.assertRaises(ValueError):
            self.calculator.add_asset("Invalid Asset", -1000)

    def test_negative_liability_value(self):
        """
        Test adding a liability with a negative value.
        """
        with self.assertRaises(ValueError):
            self.calculator.add_liability("Invalid Liability", -500)

if __name__ == "__main__":
    unittest.main()