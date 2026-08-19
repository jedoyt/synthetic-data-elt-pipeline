# The scripts here will generate a user session that simulates real-world customer journeys in an e-commerce platform.
# Each session will consist of a series of events: app_open, product_view, cart_action, and purchase events, app_close. 
# The events will be generated with realistic timestamps and attributes to mimic user behavior.

# These are the three usual outcomes of a session:
# 1. Browse and leave: The user opens the app, views some products, 
# and then leaves without making a purchase.
# 2. Cart abandonment: The user opens the app, views products, adds some to the cart, 
# but leaves without completing the purchase.
# 3. Successful purchase: The user opens the app, views products, adds some to the cart, 
# and completes a purchase from some or all of the carted items.

# Probabilites for each outcome:
# 1. Browse and leave: 70%
# 2. Cart abandonment: 20%
# 3. Successful purchase: 10%
# This produces realistic funnel metrics for the e-commerce platform, with a high number of users browsing and leaving,
# a smaller number of users adding items to the cart but not purchasing, and a small number of users completing purchases.

# Session Schema in JSON
# {
#     "session_id": "...",
#     "customer_id": 123,
#     "location_id": 45,
#     "device_type": "mobile",
#     "platform": "android",
#     "session_start_ts": "...",
#     "events": []
# }

# 4 things this session generator will do:
# 1. Choose a customer
# 2. Choose a location
# 3. Choose a session outcome
# 4. Generate events in sequence
import random
from datetime import UTC, datetime, timedelta

from customer_generator import get_random_customer
from event_generator import (
    generate_app_close_event,
    generate_app_open_event,
    generate_cart_action_event,
    generate_product_view_event,
    generate_purchase_event,
)
from faker import Faker
from location_generator import get_random_location
from product_generator import get_random_product

fake = Faker()

# helper functions
def _generate_browse_session(starting_ts, viewed_products) -> list:
    """
    Generates a user session that simulates a browsing and leaving journey in an e-commerce platform.
    The session consists of a series of events: product_views and app_close events, 
    generated with realistic timestamps and attributes to mimic user behavior.
    Returns a dictionary representing the session data, including session_id, customer_id, 
    location_id, device_type, platform, session_start_ts
    :params: starting_ts, datetime
    :params: num_product_views, int
    :return: events, list
    """
    # Start the event at app_open
    events = [generate_app_open_event(starting_ts)]
    prev_event_ts = starting_ts
    # Generate product view events. beginning with open_app
    for product in viewed_products:
        # Generate a product_view event for subsequent events
        event = generate_product_view_event(prev_event_ts, product)
        events.append(event)
        prev_event_ts = datetime.fromisoformat(event["event_ts"])

    # Append app_close event
    events.append(generate_app_close_event(prev_event_ts))

    return events

def _generate_abandoned_cart_session(starting_ts, viewed_products) -> list:
    """
    Generates a user session that simulates a cart abandonment journey in an e-commerce platform.
    The session consists of a series of events: app_open, product_view, cart_action, and app_close events, 
    generated with realistic timestamps and attributes to mimic user behavior.
    Returns a dictionary representing the session data, including session_id, 
    customer_id, location_id, device_type, platform,
    """
    # Start the event at app_open
    events = [generate_app_open_event(starting_ts)]
    
    prev_event_ts = starting_ts
    # Generate product view events. beginning with open_app

    # Randomly choose a viewed product to surely be added to cart
    chosen_index_for_add_to_cart = random.choice([viewed_products.index(prod) for prod in viewed_products])

    # Product view(s) with cart actions(s)
    for i, product in enumerate(viewed_products):
        # Generate a product_view event for subsequent events
        event = generate_product_view_event(prev_event_ts, product)
        events.append(event)
        prev_event_ts = datetime.fromisoformat(event["event_ts"])
        # Will the customer add the product to cart?
        if i == chosen_index_for_add_to_cart:
            event_2 = generate_cart_action_event(prev_event_ts, product, "add", 1)
            events.append(event_2)
            prev_event_ts = datetime.fromisoformat(event_2["event_ts"])
        else:
            add_to_cart = random.choice([True, False])
            if add_to_cart:
                event_2 = generate_cart_action_event(prev_event_ts, product, "add", 1)
                events.append(event_2)
                prev_event_ts = datetime.fromisoformat(event_2["event_ts"])

    carted_items = [item for item in events if event["event_type"] == 'cart_action']

    # Other possible cart actions
    if carted_items:
        for product in carted_items:
            action = random.choice(["none", "update", "remove"])
            if action == "none":
                continue
            if action == "update":
                updated_qty = random.randint(2, 10)
                event_3 = generate_cart_action_event(prev_event_ts, product, "update", updated_qty)
                events.append(event_3)
                prev_event_ts = datetime.fromisoformat(event_3["event_ts"])
            if action == "remove":
                event_3 = generate_cart_action_event(prev_event_ts, product, "remove", 0)
                events.append(event_3)
                prev_event_ts = datetime.fromisoformat(event_3["event_ts"])

    # Append app_close event
    events.append(generate_app_close_event(prev_event_ts))

    return events

def _generate_purchase_session(starting_ts, viewed_products):
    """
    Generates a user session that simulates a successful purchase journey in an e-commerce platform.
    The session consists of a series of events: app_open, product_view, cart_action, purchase, and app_close events, 
    generated with realistic timestamps and attributes to mimic user behavior.
    Returns a dictionary representing the session data, including session_id, customer_id, location_id, device_type, platform,
    """
    # Start the event at app_open
    events = [generate_app_open_event(starting_ts)]
    # carted_items = []
    prev_event_ts = starting_ts

    # Randomly choose a viewed product to surely be added to cart
    chosen_index_for_add_to_cart = random.choice([viewed_products.index(prod) for prod in viewed_products])

    # Generate product view event(s) with cart action(s)
    for i, product in enumerate(viewed_products):
        # Generate a product_view event for subsequent events
        event = generate_product_view_event(prev_event_ts, product)
        events.append(event)
        prev_event_ts = datetime.fromisoformat(event["event_ts"])
        # Will the customer add the product to cart?
        if i == chosen_index_for_add_to_cart:
            event_2 = generate_cart_action_event(prev_event_ts, product, "add", 1)
            events.append(event_2)
            # product["quantity"] = 1
            prev_event_ts = datetime.fromisoformat(event_2["event_ts"])
            # carted_items.append(product)
        else:
            add_to_cart = random.choice([True, False])
            if add_to_cart:
                event_2 = generate_cart_action_event(prev_event_ts, product, "add", 1)
                events.append(event_2)
                # product["quantity"] = 1
                prev_event_ts = datetime.fromisoformat(event_2["event_ts"])
                # carted_items.append(product)

    initial_cart_actions = [item for item in events if item["event_type"] == "cart_action"]

    # These placeholder lists will be used later to filter 
    # cart_action events that are potential checkout items
    
    # We'll store here the events with "update" cart action 
    updated_qty_items = [] # cart action events under "update" state

    # We'll store here the events with "remove" cart action
    removed_items = [] # cart action event under "remove" state
    
    # Other possible cart actions: update or remove
    if initial_cart_actions:
        for i, event in enumerate(initial_cart_actions):
            # Fetch full product dictionary of carted item
            product = next(prod for prod in viewed_products if prod["product_id"] == event["attributes"]["product_id"])

            action = random.choice(["none", "update", "remove"])
            if action == "none":
                continue
            if action == "update":
                updated_qty = random.randint(2, 10)
                event_3 = generate_cart_action_event(prev_event_ts, product, "update", updated_qty)
                events.append(event_3)
                prev_event_ts = datetime.fromisoformat(event_3["event_ts"])
                # Save this cart action event on updated_qty_items
                updated_qty_items.append(event)
            if action == "remove":
                if i == chosen_index_for_add_to_cart:
                    # This cart action event is chosen to stay in the cart.
                    # This should not be removed.
                    continue
                else:
                    # Generate a "remove" cart action event for this product item and set quantity to 0
                    event_3 = generate_cart_action_event(prev_event_ts, product, "remove", 0)
                    events.append(event_3)
                    prev_event_ts = datetime.fromisoformat(event_3["event_ts"])
                    # Save this cart action event on the removed_items
                    removed_items.append(event)

    # This included possible "update" and "remove" cart actions
    all_cart_actions = [item for item in events if item["event_type"] == "cart_action"]

    # Checkout/Purchase Section
    checkout_items = [] # The final list of checkout items
    potential_checkout_items = [] # Will contains valid cart_actions that can be potential checkout items

    # Gather potential checkout items
    for item in all_cart_actions:
        if item["attributes"]["action"] == "update":
            if item in removed_items:
                # Item was removed from cart. Not a potential checkout item
                continue
            else:
                # Item is a potential checkout item
                potential_checkout_items.append(item)
        if item["attributes"]["action"] == "add":
            if item in updated_qty_items or item in removed_items:
                # This "add" cart action event was followed by an "update" action
                # or was followed by a "remove" action.
                # Either way, this is cart action event is not a potential checkout item
                continue
            else:
                # This add to cart did not have any quantity update
                # nor was it removed from cart
                potential_checkout_items.append(item)

    # Randomly choose a carted item to surely be purchased
    chosen_index_for_checkout = random.choice([potential_checkout_items.index(item) for item in potential_checkout_items])

    for i, item in enumerate(potential_checkout_items):
        if i == chosen_index_for_checkout:
            for_checkout = True
        else:
            for_checkout = random.choice([True, False])
        if for_checkout:
            checkout_items.append(item)

    # Purchase transaction
    if checkout_items:
        event_4 = generate_purchase_event(prev_event_ts, checkout_items)
        events.append(event_4)
        prev_event_ts = datetime.fromisoformat(event_4["event_ts"])

    # Append app_close event
    events.append(generate_app_close_event(prev_event_ts))

    return events

# The main function
def generate_session() -> dict:
    """
    Generates a user session that simulates real-world customer journeys in an e-commerce platform.
    The session consists of a series of events: app_open, product_view, cart_action, purchase, 
    and app_close events, generated with realistic timestamps and attributes to mimic user behavior.
    The session outcome is determined probabilistically, with a 70% chance of browsing and leaving, 
    a 20% chance of cart abandonment, and a 10% chance of successful purchase.
    Returns a dictionary representing the session data, including session_id, customer_id, 
    location_id, device_type, platform, session_start_ts, and a list of events.
    """
    # Session data
    starting_ts = datetime.now(UTC) - timedelta(minutes=random.randint(0, 1440))
    random_customer = get_random_customer()
    random_location = get_random_location()
    device_dict = {
        "mobile": ["android", "ios"],
        "desktop/laptop": ["windows", "macos", "linux"],
    }
    device_type = random.choice(list(device_dict.keys()))
    platform = random.choice(device_dict[device_type])
    
    # Session dictionary
    session_dict = {
        "session_id": fake.uuid4(),
        "customer_id": random_customer['customer_id'],
        "location_id": random_location['location_id'],
        "device_type": device_type,
        "platform": platform,
        "session_start_ts": starting_ts.isoformat(timespec='seconds'),
        "events": [],
    }

    num_product_views = random.randint(1,5)
    viewed_products = []
    while len(viewed_products) < num_product_views:
        product = get_random_product()
        if product not in viewed_products:
            viewed_products.append(product)

    # Test using browse session only
    # print("Chosen browse only session.")
    # session_dict["events"].extend(_generate_browse_session(starting_ts, viewed_products))
    
    # Test using abandoned cart session only
    # print("Chosen abandonded cart session.")
    # session_dict["events"].extend(_generate_abandoned_cart_session(starting_ts, viewed_products))

    # Test using purchase session only
    # print("Chosen session with purchase.")
    # session_dict["events"].extend(_generate_purchase_session(starting_ts, viewed_products))

    roll = random.random()

    if roll < 0.70:
        print("Chosen browse only session.")
        session_dict["events"].extend(_generate_browse_session(starting_ts, viewed_products))

    elif roll < 0.90:
        print("Chosen abandonded cart session.")
        session_dict["events"].extend(_generate_abandoned_cart_session(starting_ts, viewed_products))

    else:
        print("Chosen session with purchase.")
        session_dict["events"].extend(_generate_purchase_session(starting_ts, viewed_products))

    return session_dict

# Test section
if __name__ == "__main__":
    from pprint import pprint
    # Generate a session and print the result
    session = generate_session()
    pprint(session)