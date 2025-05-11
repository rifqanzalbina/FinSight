import unittest
from finegist.tax_estimator import TaxEstimator

class TestTaxEstimator(unittest.TestCase):
    def setUp(self):
        """
        Set up an instance of TaxEstimator for testing.
        """
        self.estimator = TaxEstimator()
    
    def test_default_brackets(self):
        """
        Test that default tax brackets are initialized correctly.
        """
        self.assertGreater(len(self.estimator.tax_brackets), 0)
        self.assertTrue(all("min" in bracket and "max" in bracket and "rate" in bracket 
                            for bracket in self.estimator.tax_brackets))
    
    def test_set_tax_brackets(self):
        """
        Test setting custom tax brackets.
        """
        new_brackets = [
            {"min": 0, "max": 20000000, "rate": 0.10},
            {"min": 20000000, "max": 100000000, "rate": 0.20},
            {"min": 100000000, "max": float('inf'), "rate": 0.30}
        ]
        self.estimator.set_tax_brackets(new_brackets)
        self.assertEqual(self.estimator.tax_brackets, new_brackets)
    
    def test_invalid_tax_brackets(self):
        """
        Test that invalid tax brackets raise an error.
        """
        invalid_brackets = [
            {"minimum": 0, "maximum": 20000, "rate": 0.10}  # Wrong keys
        ]
        with self.assertRaises(ValueError):
            self.estimator.set_tax_brackets(invalid_brackets)
    
    def test_add_deduction(self):
        """
        Test adding a tax deduction.
        """
        self.estimator.add_deduction("Health Insurance", 5000000)
        self.assertEqual(len(self.estimator.deductions), 1)
        self.assertEqual(self.estimator.deductions[0]["name"], "Health Insurance")
        self.assertEqual(self.estimator.deductions[0]["amount"], 5000000)
    
    def test_invalid_deduction(self):
        """
        Test adding an invalid deduction amount.
        """
        with self.assertRaises(ValueError):
            self.estimator.add_deduction("Invalid Deduction", -1000)
    
    def test_taxable_income(self):
        """
        Test calculation of taxable income after deductions.
        """
        self.estimator.set_non_taxable_income(54000000)  # PTKP for single person
        self.estimator.add_deduction("Health Insurance", 5000000)
        
        # Gross income = 120M, Non-taxable = 54M, Deduction = 5M
        # Taxable income should be 120M - 54M - 5M = 61M
        taxable = self.estimator.taxable_income(120000000)
        self.assertEqual(taxable, 61000000)
    
    def test_calculate_tax_indonesia(self):
        """
        Test tax calculation using Indonesia's tax brackets.
        """
        # Reset to default Indonesian tax brackets
        self.estimator = TaxEstimator(country="Indonesia")
        
        # Gross income = 120M IDR
        # Non-taxable = 54M IDR
        # Taxable income = 66M IDR
        # Tax:
        # - First 60M @ 5% = 3M
        # - Remaining 6M @ 15% = 0.9M
        # Total tax = 3.9M IDR
        tax = self.estimator.calculate_tax(120000000)
        self.assertEqual(tax, 3900000)
    
    def test_tax_summary(self):
        """
        Test generating a tax summary.
        """
        self.estimator = TaxEstimator(country="Indonesia")
        self.estimator.add_deduction("Health Insurance", 5000000)
        
        summary = self.estimator.tax_summary(120000000)
        self.assertEqual(summary["gross_income"], 120000000)
        self.assertEqual(summary["non_taxable_income"], 54000000)
        self.assertEqual(summary["total_deductions"], 5000000)
        self.assertEqual(summary["taxable_income"], 61000000)
    
    def test_zero_income(self):
        """
        Test tax calculation with zero income.
        """
        tax = self.estimator.calculate_tax(0)
        self.assertEqual(tax, 0)
    
    def test_negative_income(self):
        """
        Test that negative income raises an error.
        """
        with self.assertRaises(ValueError):
            self.estimator.calculate_tax(-10000)
    
    def test_effective_tax_rate(self):
        """
        Test calculation of effective tax rate.
        """
        self.estimator = TaxEstimator(country="Indonesia")
        
        # Gross income = 120M IDR
        # Tax = 3.9M IDR (see test_calculate_tax_indonesia)
        # Effective rate = 3.9M / 120M = 0.0325 or 3.25%
        rate = self.estimator.calculate_effective_tax_rate(120000000)
        self.assertAlmostEqual(rate, 0.0325, places=4)
    
    def test_zero_income_effective_rate(self):
        """
        Test that calculating effective rate with zero income raises an error.
        """
        with self.assertRaises(ValueError):
            self.estimator.calculate_effective_tax_rate(0)

if __name__ == "__main__":
    unittest.main()