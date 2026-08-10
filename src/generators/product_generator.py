# Product generator that randomly chooses a product from products.json and returns a dictionary of the product data
import json
import random
from pathlib import Path

BASED_DIR = Path(__file__).parent
PRODUCTS_FILE = BASED_DIR / 'products.json'

with open(PRODUCTS_FILE) as f:
        PRODUCTS = json.load(f)

def get_random_product() -> dict:
    """
    Returns a dictionary representing a randomly chosen product.
    return: A dictionary containing the product data.
    """
    return random.choice(PRODUCTS)

# Test the function
# if __name__ == "__main__":
#     print(get_random_product())