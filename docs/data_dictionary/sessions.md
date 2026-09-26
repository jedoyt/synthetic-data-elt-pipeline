# Session Metadata
```
session_id
Type: TEXT, str
Descripton: Session identifier in SSID format
```
```
customer_id
Type: INTEGER, int
Description: The ID of the customer who made the session
```
```
location_id
Type: INTEGER, int
Description: The ID of the location where the customer made the session
```
```
device_type
Type: TEXT, str
Description: The type of device used by the customer to open the app
```
```
platform
Type: TEXT, str
Descripton: The type of operating system the customer's device
```
```
session_start_ts
Type: TIMESTAMP, datetime
Description: The timestamp (ISO-format) when the customer opens the app which also starts the session.
```
```
events
Type: list
Description: A list of JSON/dict objects containing the events made by the customer for the whole session.
```
## Event Metadata
```
event_id
Type: TEXT, str
Descripton: Session event identifier in SSID format
```
```
event_type
Type: TEXT, str
Description: The type of event the customer triggered within the session. 
(Event types: app_open, product_view, cart_action, purchase, app_close)
```
```
event_ts
Type: TIMESTAMP, datetime
Description: The timestamp (ISO-format) when the event happened.
```
```
attributes
Type: JSON, dict 
Description: Contains more details about the event based on event_type
```
### Event Attribute Metadata (for every `event_type`)
#### `event_type` : `app_open` or `app_close`
```
<empty dict>
Type: JSON, dict
Descripton: The events app_open and app_close do not have attributes since these are only events where the customer opens and closes the app
```
#### `event_type` : `product_view`
```
product_id
Type: INTEGER, int
Description: Product ID of the product viewed by the customer on app
```
#### `event_type` : `cart_action`
```
action
Type: TEXT, str
Description: The cart action whether the customer added ('add') an item to the cart or updated ('update') the quantity of an item on the cart.
```
```
product_id
Type: INTEGER, int
Description: ID number for product
```
```
quantity
Type: INTEGER, int
Description: The quanity of product item on cart
```
```
price
Type: FLOAT, float
Description: Price of the product
```
#### `event_type` : `purchase`
```
checkout_items
Type: list
Description: List of carted items that the customer decides to purchase.
```
```
order_id
Type: TEXT, str
Description: The order ID number of the purchase transaction.
```
```
payment_method
Type: TEXT, str
Descripton: The payment method the customer chose to settle his purchase.
```
```
shipping_fee
Type: FLOAT, float
Description: The amount of shipping fee
```
```
total_amount
Type: FLOAT, float
Description: The total amount to be paid by the customer (sub_total + shipping_fee)
```
### Checkout Item Metadata
```
product_id
Type: INTEGER, int
Description: ID number for product
```
```
quantity
Type: INTEGER, int
Description: The quanity of product item on checkout
```
```
price
Type: FLOAT, float
Description: Price of the product
```
```
sub_total
Type: FLOAT, float
Description: The total value of the checkout item by multiplying the product price by the checkout quantity.
```