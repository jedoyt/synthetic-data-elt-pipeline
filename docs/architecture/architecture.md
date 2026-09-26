# Architecture

```text
Event-Producing Operational System
                │
                ▼
         Event Store
                │
                ▼
        FastAPI REST API
                │
                ▼
           API Client
                │
                ▼
        Bronze Extraction
                │
                ▼
          Bronze Layer
         (Raw JSONL)
                │
                ▼
      Silver Transformations
                │
                ▼
          Silver Layer
              (CSV)
                │
                ▼
        Gold Warehouse
            (SQLite)
                │
                ▼
       Analytics & Insights
```

---

# Medallion Architecture

## Bronze Layer

Purpose:

Store raw events exactly as received.

Characteristics:

- Immutable
- Append-only
- Session-based
- Event-driven
- JSONL storage

Example of session data:

```json
{
    "session_id": "004d2630-5d60-4448-b0c3-5e681a969fa5", 
    "customer_id": 222, 
    "location_id": 759, 
    "device_type": "mobile", 
    "platform": "android", 
    "session_start_ts": "2026-09-24T15:10:35+00:00", 
    "events": [
        {
            "event_id": "40fc9311-8286-4472-bfeb-2e1e5b0638b7", 
            "event_type": "app_open", 
            "event_ts": "2026-09-24T15:10:35+00:00", 
            "attributes": {}
        }, 
        {
            "event_id": "e0569725-7475-4ebd-b342-8b51e32e5379", 
            "event_type": "product_view", 
            "event_ts": "2026-09-24T15:11:52+00:00", 
            "attributes": {
                "product_id": 242
            }
        }, 
        {
            "event_id": "57f00cd9-61fc-46e5-82da-ba4f40b282ae", 
            "event_type": "cart_action", 
            "event_ts": "2026-09-24T15:16:04+00:00", 
            "attributes": {
                "action": "add", 
                "product_id": 242, 
                "quantity": 1, 
                "price": 8.99
            }
        }, 
        {
            "event_id": "47817a6c-22df-4d16-a369-00139a93ad5c", 
            "event_type": "product_view", 
            "event_ts": "2026-09-24T15:16:42+00:00", 
            "attributes": {
                "product_id": 535
            }
        }, 
        {
            "event_id": "0481e76c-194a-45e3-8d6e-ea17447073b7", 
            "event_type": "product_view", 
            "event_ts": "2026-09-24T15:20:47+00:00", 
            "attributes": {
                "product_id": 305
            }
        }, 
        {
            "event_id": "68184c90-4f5d-4c41-8cef-124f2651e332", 
            "event_type": "cart_action", 
            "event_ts": "2026-09-24T15:24:54+00:00", 
            "attributes": {
                "action": "add", 
                "product_id": 305, 
                "quantity": 1, 
                "price": 199.99
            }
        }, 
        {
            "event_id": "c2786a08-5de3-4f4b-a426-67534edddf18", 
            "event_type": "product_view", 
            "event_ts": "2026-09-24T15:27:25+00:00", 
            "attributes": {
                "product_id": 405
            }
        }, 
        {
            "event_id": "bce58173-2297-4b25-8cd7-3d3db7990bf1", 
            "event_type": "product_view", 
            "event_ts": "2026-09-24T15:29:25+00:00", 
            "attributes": {
                "product_id": 255
            }
        }, 
        {
            "event_id": "390e2d11-9268-4df5-bb8f-cdb2569d7e5d", 
            "event_type": "cart_action", 
            "event_ts": "2026-09-24T15:33:03+00:00", 
            "attributes": {
                "action": "add", "product_id": 255, "quantity": 1, "price": 3.49
            }
        }, 
        {
            "event_id": "42ff23ea-4853-4e52-bafb-57819db964ed", 
            "event_type": "cart_action", 
            "event_ts": "2026-09-24T15:37:55+00:00", 
            "attributes": {
                "action": "update", "product_id": 242, "quantity": 6, "price": 8.99
            }
        }, 
        {
            "event_id": "071521ff-390c-4884-92af-a46fb4ae8564", 
            "event_type": "cart_action", 
            "event_ts": "2026-09-24T15:41:32+00:00", 
            "attributes": {
                "action": "update", "product_id": 305, "quantity": 8, "price": 199.99
            }
        }, 
        {
            "event_id": "1b97e79e-2faf-4f74-9ca4-f3121af30be0", 
            "event_type": "purchase", 
            "event_ts": "2026-09-24T15:44:07+00:00", 
            "attributes": {
                "checkout_items": [
                    {"product_id": 242, "quantity": 6, "price": 8.99, "sub_total": 53.94}
                ], 
                "order_id": "ORD-46-16329-63817", 
                "payment_method": "app_wallet", 
                "shipping_fee": 48.48, 
                "total_amount": 102.42
            }
        }, 
        {
            "event_id": "1fbbaea0-04b5-4376-a415-d54670439e09", 
            "event_type": "app_close", 
            "event_ts": "2026-09-24T15:45:01+00:00", 
            "attributes": {}
        }
    ]
}
```

---

## Silver Layer

Purpose:

Transform raw events into clean business entities.

Examples:

- Sessions
- Customers
- Orders
- Products
- Payments
- Shipments

Operations include:

- Deduplication
- Type casting
- Standardization
- Referential integrity validation

---

### Gold Layer

Purpose:

Provide analytics-ready datasets.

Examples:

- Daily Revenue
- Customer Lifetime Value
- Product Performance
- Conversion Funnel
- Cart Abandonment Analysis
- Session Analytics
