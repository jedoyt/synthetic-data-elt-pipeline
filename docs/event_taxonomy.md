# Event Taxonomy

## Why This Matters
Real companies treat event definitions as contracts.
Bad event definitions create years of analytics problems.

| Event            |
| ---------------- |
| app\_open        |
| product\_view    |
| cart\_action     |
| purchase         |
| shipment\_update |
| app\_close       |

# product_view

Description:
Customer viewed a product.

Fields:
- event_id
- session_id
- customer_id
- product_id
- event_ts

## How I might picture the raw JSON data
Here's an example of a single session generated containing all the possible events


```json
{
    "session_id": "<some-session-uuid>",
    "customer": {
        "customer_id":1,"username":"lmathou0",
        "email":"aembling0@cbslocal.com",
        "gender":"Female","age":24,"nationality":"Indonesia"
        },
    "location": {
        "city":"Wutongkou","country":"China",
        "latitude":25.84999,"longitude":115.400234
        },
    "events": [
        {
            "event_id": "<some-event-uuid>",
            "event_type": "app_open",
            "event_ts": "YYYY-MM-DDTHH:MM:SSZ"
        },
        {
            "event_id": "<some-event-uuid>",
            "event_type": "product_view",
            "event_ts": "YYYY-MM-DDTHH:MM:SSZ",
            "attributes": {
                "id":16, "category":"Gaming",
                "sub-category":"Arcade Machines & Cabinets",
                "product_name":"Arcade Game Machine",
                "description":"Retro arcade machine for classic gaming.",
                "price":299.99,
                "url":"https://pseudo-eshop.com/gaming/arcade-game-machine"
                }
        },
        {
            "event_id": "<some-event-uuid>",
            "event_type": "product_view",
            "event_ts": "YYYY-MM-DDTHH:MM:SSZ",
            "attributes": {
                "id":22, "category":"Outdoor", "sub-category":"Camping Equipment",
                "product_name":"Overnight Hiking Backpack",
                "description":"Durable backpack with ample storage for outdoor adventures.", "price":79.99,
                "url":"https://pseudo-eshop.com/outdoor/overnight-hiking-backpack"
                }
        },
        {
            "event_id": "<some-event-uuid>",
            "event_type": "product_view",
            "event_ts": "YYYY-MM-DDTHH:MM:SSZ",
            "attributes": {
                "id":28, "category":"Toys", "sub-category":"Pretend Play Toys",
                "product_name":"Wooden Children's Play Kitchen",
                "description":"Interactive kitchen set for imaginative play.",
                "price":129.99,
                "url":"https://pseudo-eshop.com/toys/wooden-children's-play-kitchen"
                }
        },
        {
            "event_id": "<some-event-uuid>",
            "event_type": "cart_action",
            "event_ts": "YYYY-MM-DDTHH:MM:SSZ",
            "attributes": {
                "id":16, "quantity": 3,
            }
        },
        {
            "event_id": "<some-event-uuid>",
            "event_type": "cart_action",
            "event_ts": "YYYY-MM-DDTHH:MM:SSZ",
            "attributes": {
                "id":22, "quantity": 2,
            }
        },
        {
            "event_id": "<some-event-uuid>",
            "event_type": "purchase",
            "event_ts": "YYYY-MM-DDTHH:MM:SSZ",
            "attributes": {
                "checkout_items": [
                        {"id":16, "quantity": 2, "sub_total": 599.98},
                        {"id":22, "quantity": 1, "sub_total": 79.99}
                    ],
                "payment_option": "debit/credit"
                "shipping_fee": 55.75,
                "total_amount": 735.72
            }
        },
        {
            "event_id": "<some-event-uuid>",
            "event_type": "app_close",
            "event_ts": "YYYY-MM-DDTHH:MM:SSZ"
        },
    ]
}
```
* Payment options can be "cash on delivery", "debit/credit", "app wallet"
