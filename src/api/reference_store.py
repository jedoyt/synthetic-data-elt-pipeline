from src.generators.customer_generator import CUSTOMERS
from src.generators.location_generator import LOCATIONS
from src.generators.product_generator import PRODUCTS


class ReferenceStore:

    def __init__(self):
        """Initialize mappings from reference entity names to fetch methods."""
        self.reference = {
            "products": self.fetch_products,
            "customers": self.fetch_customers,
            "locations": self.fetch_locations,
        }

    def fetch_products(self):
        """Return all product reference records."""
        return PRODUCTS

    def fetch_customers(self):
        """Return all customer reference records."""
        return CUSTOMERS

    def fetch_locations(self):
        """Return all location reference records."""
        return LOCATIONS