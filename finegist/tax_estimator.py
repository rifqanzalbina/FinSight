class TaxEstimator:
    def __init__(self, country="Indonesia"):
        """
        Initialize the tax estimator with default tax brackets for the specified country.
        :param country: The country whose tax system to use (default: Indonesia)
        """
        self.country = country
        self.deductions = []
        
        # Default tax brackets set to Indonesia's progressive tax rates
        if country.lower() == "indonesia":
            self.tax_brackets = [
                {"min": 0, "max": 60000000, "rate": 0.05},  # 5% for income up to 60 million IDR
                {"min": 60000000, "max": 250000000, "rate": 0.15},  # 15% for income between 60-250 million IDR
                {"min": 250000000, "max": 500000000, "rate": 0.25},  # 25% for income between 250-500 million IDR
                {"min": 500000000, "max": float('inf'), "rate": 0.30}  # 30% for income above 500 million IDR
            ]
            self.non_taxable_income = 54000000  # PTKP standard for single person in Indonesia
        else:
            # Default simple progressive tax system if country not recognized
            self.tax_brackets = [
                {"min": 0, "max": 10000, "rate": 0.10},
                {"min": 10000, "max": 50000, "rate": 0.20},
                {"min": 50000, "max": float('inf'), "rate": 0.30}
            ]
            self.non_taxable_income = 0
    
    def set_tax_brackets(self, tax_brackets):
        """
        Set custom tax brackets.
        :param tax_brackets: List of dictionaries containing min, max, and rate.
        """
        if not all("min" in bracket and "max" in bracket and "rate" in bracket for bracket in tax_brackets):
            raise ValueError("All tax brackets must contain 'min', 'max', and 'rate' keys")
        
        self.tax_brackets = tax_brackets
    
    def set_non_taxable_income(self, amount):
        """
        Set the non-taxable income amount (tax-free threshold).
        :param amount: The non-taxable amount
        """
        if amount < 0:
            raise ValueError("Non-taxable income must be non-negative")
        self.non_taxable_income = amount
    
    def add_deduction(self, name, amount):
        """
        Add a tax deduction.
        :param name: Name of the deduction
        :param amount: Amount of the deduction
        """
        if amount <= 0:
            raise ValueError("Deduction amount must be greater than zero")
        self.deductions.append({"name": name, "amount": amount})
    
    def total_deductions(self):
        """
        Calculate the total deductions.
        """
        return sum(deduction["amount"] for deduction in self.deductions)
    
    def taxable_income(self, gross_income):
        """
        Calculate the taxable income after deductions and non-taxable income.
        :param gross_income: The gross income before any deductions
        """
        if gross_income < 0:
            raise ValueError("Gross income must be non-negative")
        
        # Apply non-taxable income and deductions
        taxable = gross_income - self.non_taxable_income - self.total_deductions()
        
        # Ensure taxable income is not negative
        return max(0, taxable)
    
    def calculate_tax(self, gross_income):
        """
        Calculate the tax based on the gross income and the tax brackets.
        :param gross_income: The total income before tax
        :return: The calculated tax amount
        """
        if gross_income < 0:
            raise ValueError("Gross income must be non-negative")
        
        taxable = self.taxable_income(gross_income)
        total_tax = 0
        
        # Calculate tax for each bracket
        for bracket in self.tax_brackets:
            # Skip if income is below this bracket
            if taxable <= bracket["min"]:
                continue
            
            # Calculate the amount of income in this bracket
            bracket_income = min(taxable, bracket["max"]) - bracket["min"]
            bracket_tax = bracket_income * bracket["rate"]
            total_tax += bracket_tax
            
            # Stop if we've accounted for all income
            if taxable <= bracket["max"]:
                break
        
        return total_tax
    
    def calculate_effective_tax_rate(self, gross_income):
        """
        Calculate the effective tax rate based on the gross income.
        :param gross_income: The total income before tax
        :return: The effective tax rate as a decimal
        """
        if gross_income <= 0:
            raise ValueError("Gross income must be greater than zero")
        
        tax = self.calculate_tax(gross_income)
        return tax / gross_income
    
    def tax_summary(self, gross_income):
        """
        Generate a summary of the tax calculation.
        :param gross_income: The total income before tax
        :return: A dictionary containing tax calculation details
        """
        tax = self.calculate_tax(gross_income)
        taxable = self.taxable_income(gross_income)
        
        return {
            "gross_income": gross_income,
            "non_taxable_income": self.non_taxable_income,
            "deductions": self.deductions,
            "total_deductions": self.total_deductions(),
            "taxable_income": taxable,
            "tax_amount": tax,
            "effective_tax_rate": (tax / gross_income if gross_income > 0 else 0) * 100,
            "after_tax_income": gross_income - tax
        }