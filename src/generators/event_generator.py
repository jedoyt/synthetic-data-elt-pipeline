import random
from datetime import timedelta

import faker

fake = faker.Faker()


def generate_app_open_event(starting_ts):
    """
    Returns a dictionary representing an "app_open" 
    event with a unique event ID and timestamp.
    param starting_ts: A datetime object representing the timestamp of the event.
    return: A dictionary containing the event data.
    """
    # Return a dictionary of the event data
    return {
        "event_id": fake.uuid4(), # Generate a UUID for the event_id Ba
        "event_type": "app_open",
        "event_ts": starting_ts,
        "attributes": {}
    }

def generate_product_view_event(prev_event_ts, product_dict):
    """
    Returns a dictionary representing a "product_view" event with a unique event ID and timestamp.
    param prev_event_ts: A datetime object representing the timestamp of the previous event.
    param product_dict: A dictionary containing the product data.
    return: A dictionary containing the event data.
    """
    event = {
        "event_id": fake.uuid4(),
        "event_type": "product_view",
        "event_ts": (prev_event_ts + timedelta(seconds=random.randint(5, 300))).isoformat(timespec='seconds'),
        "attributes": {}
    }
    event["attributes"]["product_id"] = product_dict["product_id"]
    return event

def generate_cart_action_event(prev_event_ts, product_dict, action, quantity):
    """
    Returns a dictionary representing a "cart_action" event with a unique event ID and timestamp.
    param prev_event_ts: A datetime object representing the timestamp of the previous event.
    param product_dict: A dictionary containing the product data.
    param action: A string representing the action taken (e.g., "add", "update", "remove").
    param quantity: An integer representing the quantity of the product.
    return: A dictionary containing the event data.
    """ 
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

def generate_purchase_event(prev_event_ts, cart_items):
    """
    Returns a dictionary representing a "purchase" event with a unique event ID and timestamp.
    param prev_event_ts: A datetime object representing the timestamp of the previous event.
    param cart_items: A list of dictionaries containing the product data, quantity, and price.
    return: A dictionary containing the event data.
    """
    payment_method = random.choice(["debit_credit", "cash_on_delivery", "app_wallet", "digital_wallet"])
    event = {
            "event_id": fake.uuid4(),
            "event_type": "purchase",
            "event_ts": (prev_event_ts + timedelta(seconds=random.randint(5, 300))).isoformat(timespec='seconds'),
            "attributes": {
                "cart_items": []
            }
        }

    # Loop through the cart_items and add the product_id, quantity, price, and sub_total to the event attributes
    for item in cart_items:
        item_dict = {}
        item_dict["product_id"] = item["attributes"]["product_id"]
        item_dict["quantity"] = item["attributes"]["quantity"]
        item_dict["price"] = item["attributes"]["price"]
        event["attributes"]["cart_items"].append(item_dict)

            

    # Add the payment_method, shipping_fee, and total_amount to the event attributes
    event["attributes"]["order_id"] = fake.bothify('ORD-##-#####-#####').upper()
    event["attributes"]["payment_method"] = payment_method
    event["attributes"]["shipping_fee"] = random.choice([0, 5, 10, 15, 30, 50])
    total_cart_value = sum([item["price"] * item["quantity"] for item in event["attributes"]["cart_items"]])
    event["attributes"]["total_amount"] = total_cart_value + event["attributes"]["shipping_fee"]

    return event

def generate_app_close_event(prev_event_ts):
    """
    Returns a dictionary representing an "app_close" event with a unique event ID and timestamp.
    param prev_event_ts: A datetime object representing the timestamp of the previous event.
    return: A dictionary containing the event data.
    """
    return {
        "event_id": fake.uuid4(), # Generate a UUID for the event_id Ba
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
    # pprint(generate_purchase_event(datetime.now(), cart_items))  # noqa: DTZ005
