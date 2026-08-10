# Product generator that randomly chooses a product from products.json and returns a dictionary of the product data
import json
import random

with open('./src/generators/products.json') as f:
        PRODUCTS = json.load(f)

def get_random_product():
    """
    Returns a dictionary representing a randomly chosen product.
    return: A dictionary containing the product data.
    """
    return random.choice(PRODUCTS)

# Test the function
# if __name__ == "__main__":
#     print(get_random_product())