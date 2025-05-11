import requests
from datetime import datetime
import os
import json
import time

class CurrencyConverter:
    """
    Class for converting between different currencies using latest exchange rates.
    Uses a free API for getting exchange rate data.
    """
    
    def __init__(self, base_currency="USD", cache_duration=3600):
        """
        Initialize the currency converter.
        
        :param base_currency: The base currency for conversions (default: USD)
        :param cache_duration: How long to cache exchange rates in seconds (default: 1 hour)
        """
        self.base_currency = base_currency.upper()
        self.cache_duration = cache_duration
        self.rates = {}
        self.last_updated = None
        self.cache_file = os.path.join(os.path.dirname(__file__), 'cache', 'exchange_rates.json')
        
        # Create cache directory if it doesn't exist
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        
        # Try to load cached rates
        self._load_cached_rates()
    
    def _load_cached_rates(self):
        """Load exchange rates from cache file if available and not expired."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    
                if 'timestamp' in data and 'rates' in data and 'base' in data:
                    cache_age = time.time() - data['timestamp']
                    if cache_age < self.cache_duration:
                        self.rates = data['rates']
                        self.base_currency = data['base']
                        self.last_updated = datetime.fromtimestamp(data['timestamp'])
                        return True
        except Exception as e:
            print(f"Error loading cached rates: {e}")
        
        return False
        
    def _save_to_cache(self):
        """Save current rates to cache file."""
        try:
            data = {
                'timestamp': time.time(),
                'base': self.base_currency,
                'rates': self.rates
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving rates to cache: {e}")
    
    def update_rates(self):
        """Fetch the latest exchange rates from the API."""
        try:
            # Using Exchange Rate API (free tier)
            url = f"https://api.exchangerate-api.com/v4/latest/{self.base_currency}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                self.rates = data['rates']
                self.last_updated = datetime.now()
                self._save_to_cache()
                return True
            else:
                print(f"Failed to fetch exchange rates: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error updating exchange rates: {e}")
            return False
    
    def get_rate(self, from_currency, to_currency):
        """
        Get the exchange rate from one currency to another.
        
        :param from_currency: The source currency code
        :param to_currency: The target currency code
        :return: The exchange rate
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        # If rates are empty or expired, update them
        if not self.rates or (self.last_updated and 
                            (datetime.now() - self.last_updated).total_seconds() > self.cache_duration):
            self.update_rates()
        
        # If still no rates, raise exception
        if not self.rates:
            raise ValueError("Could not retrieve exchange rates")
        
        # Same currency should always return 1
        if from_currency == to_currency:
            return 1.0


        # Direct conversion if base currency
        if from_currency == self.base_currency:
            if to_currency in self.rates:
                return self.rates[to_currency]
            else:
                raise ValueError(f"Currency {to_currency} not found")
        
        # Convert from source to base, then to target
        elif from_currency in self.rates:
            # Convert from source to base first
            from_to_base = 1 / self.rates[from_currency]
            
            if to_currency == self.base_currency:
                return from_to_base
            
            elif to_currency in self.rates:
                # Convert from base to target
                return from_to_base * self.rates[to_currency]
            
            else:
                raise ValueError(f"Currency {to_currency} not found")
        
        else:
            raise ValueError(f"Currency {from_currency} not found")
    
    def convert(self, amount, from_currency, to_currency):
        """
        Convert an amount from one currency to another.
        
        :param amount: The amount to convert
        :param from_currency: The source currency code
        :param to_currency: The target currency code
        :return: The converted amount
        """
        if amount < 0:
            raise ValueError("Amount must be non-negative")
            
        rate = self.get_rate(from_currency, to_currency)
        return amount * rate
    
    def get_available_currencies(self):
        """
        Get a list of all available currencies.
        
        :return: List of currency codes
        """
        if not self.rates:
            self.update_rates()
            
        currencies = list(self.rates.keys())
        if self.base_currency not in currencies:
            currencies.append(self.base_currency)
            
        return sorted(currencies)