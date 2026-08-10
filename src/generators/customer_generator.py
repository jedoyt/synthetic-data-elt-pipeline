# Customer Generator that randomly chooses a customer from customers.json and returns a dictionary of the customer data
import json
import random
from pathlib import Path

BASED_DIR = Path(__file__).parent
CUSTOMER_FILE = BASED_DIR / 'customers.json'

with open(CUSTOMER_FILE) as f:
        CUSTOMERS = json.load(f)

def get_random_customer():
    """
    Returns a dictionary representing a randomly chosen customer.
    return: A dictionary containing the customer data.
    """
    return random.choice(CUSTOMERS)


# Test customer_generator.py
# if __name__ == "__main__":
#     print(get_random_customer())