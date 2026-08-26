from src.generators.customer_generator import CUSTOMERS
from src.generators.location_generator import LOCATIONS
from src.generators.product_generator import PRODUCTS


class ReferenceStore:

    def __init__(self):
        self.reference = {
            "products": self.fetch_products,
            "customers": self.fetch_customers,
            "locations": self.fetch_locations,
        }

    def fetch_products(self):
        return PRODUCTS

    def fetch_customers(self):
        return CUSTOMERS

    def fetch_locations(self):
        return LOCATIONS