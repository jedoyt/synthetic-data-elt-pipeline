# Sprint 1: Event-Producing Operational System (EPOS)
## Sprint Objective

Build a synthetic operational application capable of generating realistic e-commerce customer sessions.

By the end of Sprint 1, you should have:

✅ Synthetic customers

✅ Synthetic products

✅ Synthetic sessions

✅ Event generation logic

✅ A session lifecycle

✅ JSON event records

✅ Ability to generate N sessions on demand

## Why We Start Here

Remember our architecture:
```
Event-Producing Operational System
           ↓
      REST API
           ↓
     Bronze Layer
           ↓
       Warehouse
```

The pipeline is only as good as its source.

Before we build APIs, Bronze layers, or SQL models, we need a believable stream of events.

## Sprint 1 Deliverables

There are 5 subcomponents.

### 1. Reference Data
Goal

Create relatively static business entities.

These are your "master data".

`customers.json`

Generate:
```json
{
  "customer_id": "C000001",
  "customer_name": "John Doe",
  "email": "john@email.com",
  "city": "Manila",
  "created_at": "2026-01-01T00:00:00Z"
}
```

Target:
```
1000 customers
```
`products.json`

Generate:
```json
{
  "product_id": "P000001",
  "product_name": "Wireless Mouse",
  "category": "Electronics",
  "price": 29.99
}
```

Target:
```
100 products
```
#### Why?

Customers and products should exist before sessions.

### 2. Event Taxonomy

One of the most important artifacts in the entire project.

Create:
```
docs/event_taxonomy.md
```

Define:

| Eventapp_open |
| --- |
| product_view |
| cart_action |
| purchase |
| shipment_update |
| app_close |

For each event document:
```
# product_view

Description:
Customer viewed a product.

Fields:
- event_id
- session_id
- customer_id
- product_id
- event_ts
```
#### Why This Matters

Real companies treat event definitions as contracts.

Bad event definitions create years of analytics problems.

### 3. Session Generator

This is the heart of Sprint 1.

Create:
```
src/generators/session_generator.py
```

Think of a customer session as:
```
app_open
      ↓
product_view
      ↓
product_view
      ↓
cart_action
      ↓
purchase
      ↓
app_close
```

Not every session should purchase.

For realism:
```
70% browse only

20% cart

10% purchase
```

Example:

Session A
```
open
view
view
close
```

Session B
```
open
view
cart
close
```

Session C
```
open
view
view
cart
purchase
close
```

This variation later enables:

* Funnel analytics
* Conversion rates
* Cart abandonment

### 4. Standard Event Schema

Every event must share a common structure.

Create:
```json
{
    "event_id": "...",
    "session_id": "...",
    "customer_id": "...",
    "event_type": "...",
    "event_ts": "...",
    "attributes": {}
}
```

Example
```json
{
  "event_id": "EVT001",
  "session_id": "S001",
  "customer_id": "C001",
  "event_type": "product_view",
  "event_ts": "2026-08-04T10:00:00Z",
  "attributes": {
    "product_id": "P001"
  }
}
```
#### Why Use attributes?

New event types become easy.

Example:
```json
{
  "event_type": "purchase",
  "attributes": {
    "order_amount": 2500,
    "payment_method": "GCash"
  }
}
```

Later:
```json
{
  "event_type": "review"
}
```

requires zero schema changes.

### 5. Event Batch Generator

Create:
```
src/generators/generate_batch.py
```

Function:
```python
generate_sessions(
    session_count=100
)
```

Returns:
```
List[events]
```

Output Example
```
250
events generated

100
sessions generated
```

Save sample output to:
```
data/sample/
```

Example:
```
sample_events.json
```

This is NOT Bronze yet.

This is just proving the EPOS works.

## Recommended Sprint 1 Folder Additions
```
src/

└── generators/
    ├── customer_generator.py
    ├── product_generator.py
    ├── session_generator.py
    └── generate_batch.py
```
## Sprint 1 Acceptance Criteria

I will consider Sprint 1 complete when you can run:
```
python src/generators/generate_batch.py
```

and produce output resembling:
```
100 customers loaded

100 products loaded

100 sessions generated

642 events generated
```

along with:
```json
[
  {
    "event_id": "...",
    "event_type": "app_open"
  },
  {
    "event_id": "...",
    "event_type": "product_view"
  },
  {
    "event_id": "...",
    "event_type": "cart_action"
  }
]
```
## Coach's Advice for Sprint 1

There is one temptation I want you to resist:

❌ Don't build Flask/FastAPI yet.

❌ Don't build the pseudo REST API yet.

❌ Don't build Bronze ingestion yet.

For this sprint:
```
Focus:
Generate believable sessions
```

The API layer will become much easier once the session generator is stable.

Think of Sprint 1 as building the "engine" before building the "gas station."

Once you've completed Sprint 1, we'll do a proper design review and then move into the pseudo REST API and Bronze ingestion in Sprint 2.