import unittest
from unittest.mock import patch, MagicMock
from finegist.currency_converter import CurrencyConverter

class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        """
        Set up an instance of CurrencyConverter for testing with mocked API responses.
        """
        self.converter = CurrencyConverter()
        
    @patch('finegist.currency_converter.requests.get')
    def test_update_rates(self, mock_get):
        """
        Test updating exchange rates from the API.
        """
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'base': 'USD',
            'rates': {
                'EUR': 0.85,
                'GBP': 0.75,
                'JPY': 110.0,
                'IDR': 14500.0
            }
        }
        mock_get.return_value = mock_response
        
        # Call update_rates and check the result
        result = self.converter.update_rates()
        self.assertTrue(result)
        self.assertEqual(self.converter.rates['EUR'], 0.85)
        self.assertEqual(self.converter.rates['GBP'], 0.75)
        self.assertEqual(self.converter.rates['JPY'], 110.0)
        
    def test_get_rate_same_currency(self):
        """
        Test getting the exchange rate between the same currency.
        """
        # Set mock rates for testing
        self.converter.rates = {
            'EUR': 0.85,
            'GBP': 0.75,
            'JPY': 110.0,
            'IDR': 14500.0
        }
        self.converter.base_currency = 'USD'
        
        # Same currency should have a rate of 1
        self.assertEqual(self.converter.get_rate('USD', 'USD'), 1)
        
    @patch('finegist.currency_converter.requests.get')
    def test_convert_amount(self, mock_get):
        """
        Test converting an amount from one currency to another.
        """
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'base': 'USD',
            'rates': {
                'EUR': 0.85,
                'GBP': 0.75,
                'JPY': 110.0,
                'IDR': 14500.0
            }
        }
        mock_get.return_value = mock_response
        
        # Update rates
        self.converter.update_rates()
        
        # Test conversion
        # 100 USD = 85 EUR
        self.assertAlmostEqual(self.converter.convert(100, 'USD', 'EUR'), 85)
        
        # 100 EUR to USD = 100 / 0.85 = ~117.65 USD
        self.assertAlmostEqual(self.converter.convert(100, 'EUR', 'USD'), 117.65, places=2)
        
        # 100 EUR to GBP = (100 / 0.85) * 0.75 = ~88.24 GBP
        self.assertAlmostEqual(self.converter.convert(100, 'EUR', 'GBP'), 88.24, places=2)
        
    def test_negative_amount(self):
        """
        Test converting a negative amount.
        """
        with self.assertRaises(ValueError):
            self.converter.convert(-100, 'USD', 'EUR')
            
    @patch('finegist.currency_converter.requests.get')
    def test_get_available_currencies(self, mock_get):
        """
        Test getting a list of available currencies.
        """
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'base': 'USD',
            'rates': {
                'EUR': 0.85,
                'GBP': 0.75,
                'JPY': 110.0,
                'IDR': 14500.0
            }
        }
        mock_get.return_value = mock_response
        
        # Update rates
        self.converter.update_rates()
        
        # Test available currencies
        currencies = self.converter.get_available_currencies()
        self.assertIn('USD', currencies)
        self.assertIn('EUR', currencies)
        self.assertIn('GBP', currencies)
        self.assertIn('JPY', currencies)
        self.assertIn('IDR', currencies)
        self.assertEqual(len(currencies), 5)

if __name__ == "__main__":
    unittest.main()