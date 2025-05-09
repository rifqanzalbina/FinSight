class NetWorthCalculator:
    def __init__(self):
        """
        Initialize the net worth calculator with empty lists for assets and liabilities.
        """
        self.assets = []
        self.liabilities = []

    def add_asset(self, name, value):
        """
        Add an asset to the calculator.
        :param name: Name of the asset.
        :param value: Value of the asset.
        """
        if value < 0:
            raise ValueError("Asset value must be non-negative.")
        self.assets.append({"name": name, "value": value})

    def add_liability(self, name, value):
        """
        Add a liability to the calculator.
        :param name: Name of the liability.
        :param value: Value of the liability.
        """
        if value < 0:
            raise ValueError("Liability value must be non-negative.")
        self.liabilities.append({"name": name, "value": value})

    def total_assets(self):
        """
        Calculate the total value of all assets.
        """
        return sum(asset["value"] for asset in self.assets)

    def total_liabilities(self):
        """
        Calculate the total value of all liabilities.
        """
        return sum(liability["value"] for liability in self.liabilities)

    def calculate_net_worth(self):
        """
        Calculate the net worth (assets - liabilities).
        """
        return self.total_assets() - self.total_liabilities()