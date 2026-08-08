# Event Taxonomy

## Why This Matters

Real companies treat event definitions as contracts.

Poorly designed events can lead to years of reporting inconsistencies, difficult transformations, and unreliable analytics.

This document defines the source event model for the Synthetic E-Commerce Analytics ELT Pipeline.

The goal is to create realistic user behavior that can later be transformed into analytics-ready business entities through ELT processes.

---

# Event Hierarchy

```text
Customer
    │
    ▼
Session
    │
    ▼
Events
    ├── app_open
    ├── product_view
    ├── cart_action
    ├── purchase
    ├── shipment_update
    └── app_close
```

---

# Reference Data

The following entities are considered master/reference data and are generated independently from user sessions.

## Customers

Stored separately.

Example:

```json
{
    "customer_id": 1,
    "username": "lmathou0",
    "email": "aembling0@cbslocal.com",
    "gender": "Female",
    "age": 24,
    "nationality": "Indonesia",
    "created_at": "2026-08-01T00:00:00Z"
}
```

---

## Products

Stored separately.

Example:

```json
{
    "product_id": 16,
    "category": "Gaming",
    "sub_category": "Arcade Machines & Cabinets",
    "product_name": "Arcade Game Machine",
    "description": "Retro arcade machine for classic gaming.",
    "price": 299.99,
    "url": "https://pseudo-eshop.com/gaming/arcade-game-machine"
}
```

---

## Locations

Stored separately.

Example:

```json
{
    "location_id": 101,
    "city": "Wutongkou",
    "country": "China",
    "latitude": 25.84999,
    "longitude": 115.400234
}
```

---

# Session Schema

A session represents a customer's interaction with the platform.

Example:

```json
{
    "session_id": "<session-uuid>",
    "customer_id": 1,
    "location_id": 101,
    "device_type": "mobile",
    "platform": "android",
    "session_start_ts": "YYYY-MM-DDTHH:MM:SSZ",
    "events": []
}
```

---

# Standard Event Schema

Every event must conform to the same structure