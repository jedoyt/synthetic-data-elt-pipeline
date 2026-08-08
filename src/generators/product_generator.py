# Product generator that randomly chooses a product from products.json and returns a dictionary of the product data
import json
import random


with open('products.json') as f:
        PRODUCTS = json.load(f)

def generate_product():
    
    product = random.choice(PRODUCTS)
    return product