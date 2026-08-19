import random
from datetime import datetime, timedelta

import faker

fake = faker.Faker()


def generate_app_open_event(starting_ts) -> dict:
    """
    Returns a dictionary representing an "app_open" 
    event with a unique event ID and timestamp.
    param starting_ts: A datetime object representing the timestamp of the event.
    return: A dictionary containing the event data.
    """
    # Ensure starting_ts is a datetime object
    try:
        assert isinstance(starting_ts, datetime)
    except AssertionError:
        starting_ts = datetime.fromisoformat(starting_ts)
        
    # Return a dictionary of the event data
    return {
        "event_id": fake.uuid4(), # Generate a UUID for the event_id
        "event_type": "app_open",
        "event_ts": starting_ts.isoformat(timespec='seconds'),
        "attributes": {}
    }

def generate_product_view_event(prev_event_ts, product_dict) -> dict:
    """
    Returns a dictionary representing a "product_view" event with a unique event ID and timestamp.
    param prev_event_ts: A datetime object representing the timestamp of the previous event.
    param product_dict: A dictionary containing the product data.
    return: A dictionary containing the event data.
    """
    # Ensure prev_event_ts is a datetime object
    try:
        assert isinstance(prev_event_ts, datetime)
    except AssertionError:
        prev_event_ts = datetime.fromisoformat(prev_event_ts)
        
    # Create and return dictionary of the event data
    event = {
        "event_id": fake.uuid4(),
        "event_type": "product_view",
        "event_ts": (prev_event_ts + timedelta(seconds=random.randint(5, 300))).isoformat(timespec='seconds'),
        "attributes": {}
    }
    event["attributes"]["product_id"] = product_dict["product_id"]
    return event

def generate_cart_action_event(prev_event_ts, product_dict, action, quantity) -> dict:
    """
    Returns a dictionary representing a "cart_action" event with a unique event ID and timestamp.
    param prev_event_ts: A datetime object representing the timestamp of the previous event.
    param product_dict: A dictionary containing the product data.
    param action: A string representing the action taken (e.g., "add", "update", "remove").
    param quantity: An integer representing the quantity of the product.
    return: A dictionary containing the event data.
    """ 
    # Ensure prev_event_ts is a datetime object
    try:
        assert isinstance(prev_event_ts, datetime)
    except AssertionError:
        prev_event_ts = datetime.fromisoformat(prev_event_ts)
        
    # Create and return a dictionary of the event data
    event = {
        "event_id": fake.uuid4(),
        "event_type": "cart_action",
        "event_ts": (prev_event_ts + timedelta(seconds=random.randint(5, 300))).isoformat(timespec='seconds'),
        "attributes": {}
    }
    event["attributes"]["action"] = action
    event["attributes"]["product_id"] = product_dict["product_id"]
    event["attributes"]["quantity"] = quantity
    event["attributes"]["price"] = product_dict["price"]

    return event

def generate_purchase_event(prev_event_ts, checkout_items) -> dict:
    """
    Returns a dictionary representing a "purchase" event with a unique event ID and timestamp.
    param prev_event_ts: A datetime object representing the timestamp of the previous event.
    param checkout_items: A list of dictionaries containing the product data, quantity, and price.
    return: A dictionary containing the event data.
    """
    # Ensure prev_event_ts is a datetime object
    try:
        assert isinstance(prev_event_ts, datetime)
    except AssertionError:
        prev_event_ts = datetime.fromisoformat(prev_event_ts)
        
    # Create and return a dictionary of the event data
    payment_method = random.choice(["debit_credit", "cash_on_delivery", "app_wallet"])
    event = {
            "event_id": fake.uuid4(),
            "event_type": "purchase",
            "event_ts": (prev_event_ts + timedelta(seconds=random.randint(5, 300))).isoformat(timespec='seconds'),
            "attributes": {
                "checkout_items": []
            }
        }

    # Loop through the checkout_items and add the product_id, quantity, price, and sub_total to the event attributes
    for item in checkout_items:
        item_dict = {}
        item_dict["product_id"] = item["attributes"]["product_id"]
        item_dict["quantity"] = item["attributes"]["quantity"]
        item_dict["price"] = item["attributes"]["price"]
        item_dict["sub_total"] = round(item["attributes"]["quantity"] * item["attributes"]["price"], 2)
        event["attributes"]["checkout_items"].append(item_dict)

    # Add the payment_method, shipping_fee, and total_amount to the event attributes
    event["attributes"]["order_id"] = fake.bothify('ORD-##-#####-#####').upper()
    event["attributes"]["payment_method"] = payment_method
    event["attributes"]["shipping_fee"] = round(random.uniform(5, 50), 2)
    total_cart_value = sum([item["price"] * item["quantity"] for item in event["attributes"]["checkout_items"]])
    event["attributes"]["total_amount"] = round(total_cart_value + event["attributes"]["shipping_fee"],2)

    return event

def generate_app_close_event(prev_event_ts) -> dict:
    """
    Returns a dictionary representing an "app_close" event with a unique event ID and timestamp.
    param prev_event_ts: A datetime object representing the timestamp of the previous event.
    return: A dictionary containing the event data.
    """
    # Ensure prev_event_ts is a datetime object
    try:
        assert isinstance(prev_event_ts, datetime)
    except AssertionError:
        prev_event_ts = datetime.fromisoformat(prev_event_ts)

    # Return a dictionary of the event data
    return {
        "event_id": fake.uuid4(), # Generate a UUID for the event_id
        "event_type": "app_close",
        "event_ts": (prev_event_ts + timedelta(seconds=random.randint(5, 300))).isoformat(timespec='seconds'),
        "attributes": {}
    }


# Test event_generator.py
# if __name__ == "__main__":
#     from datetime import datetime
#     from pprint import pprint

    # Test generate_app_open_event and app_close_event
    # pprint(generate_app_open_event(fake.date_time_this_year()))
    # pprint(generate_app_close_event(fake.date_time_this_year()))

    # from product_generator import get_random_product

    # # Test generate_product_view_event
    # product = get_random_product()
    # pprint(product)
    # pprint(generate_product_view_event(fake.date_time_this_year(), product))

    # Test generate_cart_action_event
    # pprint(generate_cart_action_event(fake.date_time_this_year(), product, "add", 2))

    # Test generate_purchase_event
    # products = [ get_random_product() for _ in range(3) ]
    # print("Products to cart:")
    # pprint(products)
    # print("\nCart items:")
    # cart_items = [ generate_cart_action_event(fake.date_time_this_year(), product, "add", 2) for product in products ]
    # pprint(generate_purchase_event(datetime.now(), cart_items))
