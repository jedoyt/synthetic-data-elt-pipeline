# Customer Generator that randomly chooses a customer from customers.json and returns a dictionary of the customer data
import json
import random


with open('customers.json') as f:
        CUSTOMERS = json.load(f)

def generate_customer():
    customer = random.choice(CUSTOMERS)
    return customer