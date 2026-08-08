# Customer Generator that randomly chooses a customer from customers.json and returns a dictionary of the customer data
import json
import random


def generate_customer():
    with open('customers.json') as f:
        customers = json.load(f)
    customer = random.choice(customers)
    return customer