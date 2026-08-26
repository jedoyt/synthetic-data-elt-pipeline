from src.generators.customer_generator import CUSTOMERS
from src.generators.location_generator import LOCATIONS
from src.generators.product_generator import PRODUCTS


class ReferenceStore:

    def __init__(self):
        self.reference = {
            "products": self._products,
            "users": self._users,
            "locations": self._locations,
        }

    def _products(self):
        return PRODUCTS

    def _users(self):
        return CUSTOMERS

    def _locations(self):
        return LOCATIONS