# Product generator that randomly chooses a product from products.json and returns a dictionary of the product data
import json
import random


def generate_product():
    with open('products.json') as f:
        products = json.load(f)
    product = random.choice(products)
    return product