# Guiding Philosophy

One thing I want you to remember throughout this project:

We are not building an e-commerce platform.

We are building a miniature analytics platform that happens to use e-commerce event data.

Many beginners accidentally spend:
```
80% building the application
20% building the pipeline
```

We want:
```
20% application simulation
80% data engineering
```

The Event-Producing Operational System only exists to feed our ELT pipeline.

# Learning Roadmap

We'll build this project in 8 phases.

Each phase produces something usable and portfolio-worthy.
```
Phase 0  Foundation & Repository
Phase 1  Event-Producing Operational System
Phase 2  Bronze Layer
Phase 3  SQLite Warehouse Loading
Phase 4  Silver Layer Modeling
Phase 5  Gold Layer Analytics
Phase 6  Pipeline Operations
Phase 7  Portfolio Packaging
```

# Phase 0: Foundation & Repository
Learning Goal

Learn how professional data projects are structured.

Deliverable

Repository skeleton.

## Folder Structure
```
synthetic-ecommerce-analytics/

├── README.md

├── configs/
│   ├── api_config.json
│   ├── pipeline_config.json

├── data/
│
│   ├── bronze/
│   ├── warehouse/
│   ├── exports/

├── docs/
│   ├── architecture/
│   ├── diagrams/
│   ├── data_dictionary/

├── logs/

├── src/
│
│   ├── generators/
│   ├── api/
│   ├── extract/
│   ├── load/
│   ├── transform/
│   ├── quality/
│   ├── metadata/
│   ├── orchestrator/

├── sql/
│
│   ├── raw/
│   ├── silver/
│   ├── gold/

├── tests/

└── requirements.txt
```

## What You'll Learn
* Repository organization
* Separation of concerns
* Configuration-driven pipelines

# Phase 1: Event-Producing Operational System
## Learning Goal

Understand the difference between operational systems and analytics systems.

## Deliverable

A Python application that continuously generates user sessions.

## Generated Workflow

Example:
```
app_open

product_view

product_view

cart_action

purchase

app_close
```

## Event Schema
### Required Fields
```json
{
  "event_id": "",
  "session_id": "",
  "customer_id": "",
  "event_type": "",
  "event_ts": "",
  "product_id": "",
  "quantity": 0
}
```

## Learning Concepts
### Event Data

Not:
```
Order 123
```

Instead:
```
Customer viewed product
Customer added cart
Customer purchased
```
### Event Sourcing Mindset

You'll eventually reconstruct:
```
Orders
Payments
Sessions
```

from events.

This is a powerful concept.

# Phase 2: Bronze Layer
## Learning Goal

Learn ingestion patterns.

## Deliverable

Raw JSONL event files.

Example:
```
data/bronze/

events_2026-08-03-130000.jsonl
events_2026-08-03-131000.jsonl
events_2026-08-03-132000.jsonl
```
Rule

Bronze NEVER cleans data.

Bad:
```python
if product_id is None:
    skip_record
```

Good:
```python
write_everything()
```

## Why?

Data Engineers preserve history.

Bronze equals truth.

# Phase 3: SQLite Warehouse Loading
## Learning Goal

Learn warehouse loading.

## Deliverable

Raw warehouse tables.

## Example Tables
```
raw_events
```
```
pipeline_metadata
```
## Metadata Table

Very important.

Example:
```sql
CREATE TABLE pipeline_metadata(
    pipeline_name TEXT,
    last_processed_ts TEXT,
    status TEXT
);
```

Now you'll learn:
```
Incremental Loads
```
# Phase 4: Silver Layer Modeling

This phase is where Data Engineering begins.

## Learning Goal

Transform chaos into business meaning.

## Input
```
raw_events
```

## Output
```
silver_sessions

silver_orders

silver_customers

silver_products

silver_payments

silver_shipments
```
## Example

Bronze:
```json
{
 "event_type":"purchase"
}
```

Silver:
```
silver_orders
```

contains:
```
order_id
customer_id
amount
order_ts
```

## Skills
### SQL CTEs
```sql
WITH purchases AS (...)
```

### Window Functions
```sql
ROW_NUMBER()
```

Aggregations
```sql
GROUP BY
```

Deduplication
```sql
DISTINCT
```

This phase provides the highest SQL growth.

# Phase 5: Gold Layer Analytics

Now we answer business questions.

## Deliverables
**`gold_daily_revenue`**
```
date
revenue
```

**`gold_customer_ltv`**
```
customer
lifetime_value
```

**`gold_conversion_funnel`**
```
app_open
product_view
cart_action
purchase
```

**`gold_cart_abandonment`**
```
added_to_cart
not_purchased
```

**`gold_session_metrics`**
```
avg_session_duration
conversion_rate
```

## Skills

You'll learn how analytics teams think.

Not:
```
How many records?
```

But:
```
What story do the records tell?
```
# Phase 6: Pipeline Operations

This phase is what separates scripts from pipelines.

## Learning Goal

Build production-like fundamentals.

## Deliverables
### Logging
```
logs/pipeline.log
```

### Retry Logic
```python
for attempt in range(3):
```

### Metadata Tracking
```
pipeline_metadata
```

### Data Quality Checks

Examples:
```sql
session_id IS NOT NULL
```
```sql
quantity > 0
```

### Pipeline Runs Table
```
pipeline_runs
```

Tracks:
```
start_time
end_time
status
rows_processed
```

# Phase 7: Portfolio Packaging

Most learners skip this.

Don't.

## Deliverables
### README

Include:

* Problem
* Architecture
* Tech Stack
* Pipeline Flow
* Sample Outputs

### Architecture Diagram

Simple but professional.

### ERD

Show:
```
raw
silver
gold
```
relationships.

### Data Dictionary

Every table.

Every column.

Business definition.

### Demo Walkthrough

A hiring manager should understand:
```
What it does

Why it exists

How you built it
```

within 5 minutes.