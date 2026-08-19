# Project Charter

## Project Title

Synthetic E-Commerce Analytics ELT Pipeline using Python, SQLite, and Medallion Architecture

---

## Project Overview

This project aims to build an end-to-end ELT (Extract, Load, Transform) analytics platform that ingests synthetic e-commerce user activity generated from an Event-Producing Operational System.

The platform will simulate a real-world e-commerce application where customers interact with products through user sessions and application events. These events will be exposed through a pseudo REST API and ingested into a Medallion Architecture consisting of Bronze, Silver, and Gold layers.

Raw event data will first be stored without modification in the Bronze layer. The data will then be loaded into SQLite and transformed using SQL scripts to produce clean business entities and analytics-ready datasets.

The project is designed to strengthen foundational Data Engineering skills through hands-on implementation of:

- ELT Architecture
- SQL-based data transformations
- Medallion Architecture
- Incremental loading
- Data quality validation
- Dimensional modeling
- Pipeline orchestration
- Analytics engineering principles

---

# Business Problem

An e-commerce company wants to better understand customer behavior throughout the shopping journey.

Although operational systems generate large amounts of user activity data, the company lacks a centralized analytics platform capable of answering key business questions regarding:

- User engagement
- Product discovery
- Cart activity
- Purchase conversion
- Customer retention
- Revenue generation
- Product performance
- Delivery performance

The objective of this project is to build a reliable ELT analytics platform that transforms raw customer interaction events into business insights.

---

# Project Objectives

## Primary Objectives

- Build a complete ELT pipeline.
- Practice loading raw data prior to transformation.
- Develop strong SQL transformation skills.
- Implement Medallion Architecture.
- Model event-based user activity data.
- Design dimensional models for analytics.
- Implement incremental load processing.
- Create a maintainable project structure using Python and SQL.

## Secondary Objectives

- Learn data quality validation techniques.
- Practice pipeline logging and monitoring.
- Implement simple orchestration logic.
- Develop portfolio-ready engineering documentation.
- Learn customer journey analytics concepts.
- Learn session-based data modeling techniques.

---

# Scope

## Data Generation: Event-Producing Operational System

Synthetic operational system built with:

- Python
- Faker (dynamic user and event generation)
- Mockaroo (optional generation of static reference data)

Reference datasets may include:

- Geographic locations
- Shipping regions
- Product catalog
- Product categories
- Payment methods

These datasets will be stored as JSON files and used by the event generation service.

### Business Entities

- Customers
- Products
- Orders
- Order Items
- Payments
- Shipments

### User Activity Events

- app_open
- product_view
- cart_action
- payment
- purchase
- shipment_update
- delivery_confirmation
- app_close

---

## Data Ingestion

Python extraction processes that:

- Call pseudo API endpoints
- Retrieve JSON payloads
- Store raw event records
- Maintain ingestion metadata
- Support incremental ingestion

---

## Data Storage

### Bronze

JSONL Files

### Silver

SQLite

### Gold

SQLite

---

## Data Transformation

Transformations will be written entirely in SQL scripts.

No ORM-based transformations will be used.

Example:

```sql
SELECT
    customer_id,
    COUNT(*) AS total_orders
FROM silver_orders
GROUP BY customer_id;
```

---

## Analytics Outputs

Gold marts will support:

- Revenue Analysis
- Customer Lifetime Value
- Customer Conversion Analysis
- Product Performance Analysis
- Session Analytics
- Cart Abandonment Analysis
- Order Fulfillment Analysis
- Payment Method Analysis

---

# Out of Scope

The following technologies are intentionally excluded from the initial implementation:

- Cloud Platforms-- Airflow
- Docker
- Kubernetes
- Kafka
- Spark
- Snowflake
- Databricks
- dbt
- Machine Learning

Some implementation patterns may resemble these technologies for learning purposes.

These technologies may be explored in future project phases.
---

# Stakeholders

## Primary Stakeholder

Data Engineering Learner

Purpose:

- Skill development
- Portfolio development

## Secondary Stakeholder

Analytics Consumers

Consumes:

- Revenue metrics
- Customer metrics
- Product metrics
- Behavioral analytics
- Operational analytics

---

# Data Sources

## Source Type

Synthetic Event-Producing Operational System

## Generation Method

Python service using Faker and optional Mockaroo reference datasets.

---

## Access Method

Pseudo REST API

Example endpoints:

```http
GET /sessions
GET /events
GET /customers
GET /products
GET /orders
GET /payments
GET /shipments
```

---

## Update Frequency

Continuous synthetic generation at configurable intervals.

Example:

```text
Every 10 seconds
```

---

# Architecture

```text
Event-Producing Operational System
                │
        Pseudo REST API
                │
                ▼
         Extract Layer
            (Python)
                │
          Bronze Layer
        (Raw JSONL Events)
                │
                ▼
            Raw SQLite
                │
                ▼
          Silver Layer
      (SQL Transformations)
                │
                ▼
           Gold Layer
       (Analytics Marts)
                │
                ▼
        Business Insights
```

---

# Medallion Architecture

## Bronze Layer

### Purpose

Store source data exactly as received.

### Characteristics

- Immutable
- Append-only
- Event-based
- Session-oriented
- Raw JSONL

### Example Files

```text
events_sessions_2026-08-03T10-00-00Z.jsonl
events_sessions_2026-08-03T10-10-00Z.jsonl
events_sessions_2026-08-03T10-20-00Z.jsonl
```

### Session Structure

Each session may contain:

- session_id
- customer_id
- location-- device information
- event timestamps
- customer actions

### Supported Events

- app_open
- product_view
- cart_action
- payment
- purchsse
- shipment_update
- delivery_confirmation
- app_close

No transformations are performed in Bronze.

---

## Silver Layer

### Purpose

Convert raw event data into clean business entities and standardized event models.

### Operations

- Deduplication
- Data type casting
- Null handling
- Standardization
- Referential integrity validation
- Event normalization
- Session reconstruction

### Example Tables

```text
silver_sessions
silver_events
silver_customers
silver_products
silver_orders
silver_payments
silver_shipments
```

Silver represents the operational business view.

---

## Gold Layer

### Purpose

Provide analytics-ready models designed to answer business questions.

### Dimensional Models

```text
fact_orders
fact_sessions
fact_payments

dim_customer
dim_product
dim_location
dim_date
```

### Analytics Marts

```text
gold_daily_revenue
gold_customer_ltv
gold_repeat_customers
gold_product_performance
gold_conversion_funnel
gold_cart_abandonment
gold_session_metrics
gold_order_fulfillment
```

Gold represents the analytical business view.

---

# ELT Strategy

## Extract

Retrieve data from pseudo API endpoints.

---

## Loads
Store records into:

- Bronze JSONL files
- Raw SQLite tables

without modification.

---

## Transforms
Execute SQL scripts against SQLite.

```text
sql/
├── raw/
├── silver/
├── gold/
```

All transformations occur after data loading.

This project follows a true ELT architecture.

---

# Data Quality Requirements

## Completeness

Required fields include:

- session_id
- customer_id
- event_ts
- event_type

---
### Uniqueness

Unique identifiers include:

- session_id
- customer_id
- order_id
- payment_id
- shipment_id

---

## Validity

Examples:

```sql
quantity > 0
amount >= 0
event_ts IS NOT NULL
event_type IS NOT NULL
```

---

## Referential Integrity

Examples:

```text
order.customer_id
must exist in
customer.customer_id
```

```text
event.session_id
must exist in
session.session_id
```

---

# Incremental Loading Strategy

## Approach

Watermark-based loading.

### Tracked Fields

```text
created_at
updated_at
event_ts
```

### Metadata Table

```text
pipeline_metadata
```

Stores:

- Previous execution time
- Latest processed timestamp
- Execution status-- Rows extracted
- Rows loaded
- Rows transformed

---

# Business Questions

The Gold layer should answer the following questions:

### Revenue & Sales

- What is the daily revenue trend?
- What is the average order value?
- Which products generate the most revenue?

### Customer Analytics

- Who are the highest value customers?
- Which customers are repeat buyers?
- What is the customer lifetime value?

### Product Analytics

- Which products are most viewed?
- Which products are most purchased?
- Which product categories drive the most sales?

### Customer Journey Analytics

- How many sessions result in purchases?
- What is the purchase conversion rates
- Where do customers drop off in the funnel?
- Which products are frequently abandoned in carts?

### Operational Analytics

- What percentage of orders are delivered on time?
- Which payment methods are most frequently used?

---

# Success Criteria

The project is considered successful when:

- Synthetic events are continuously generated.
- Session-based activity can be retrieved through pseudo API endpoints.
- Raw event data is stored in Bronze JSONL files.
- Raw data is loaded into SQLite.
- SQL transformations create Silver datasets.
- SQL transformations create Gold marts.
- Incremental loading works correctly.
- Data quality checks are implemented.
- Pipeline execution logging works correctly.
- Full project documentation is completed.

---

# Deliverables

## Code Deliverables

```text
src/
├── api/
├── generators/
├── extract/
├── load/
├── sql/
│   ├── raw/
│   ├── silver/
│   └── gold/
├── logs/
├── config/
└── tests/
```

---

## Technical Deliverables

- Working ELT pipeline
- Event generation service
- Pseudo REST API
- SQL transformation layer
- SQLite warehouse
- Incremental loading mechanism
- Data quality framework
- Logging framework

---

## Portfolio Deliverables

- Architecture Diagram
- README
- Data Dictionary
- Pipeline Flow Diagram
- Entity Relationship Diagram (ERD)
- Analytics Mart Documentation
- Sample Business Queries
- Project Walkthrough Documentation

---

# Future Enhancements (Phase 2)

Once the foundation is complete, the project can evolve into:

- Custom Python Orchestrator
- Scheduling System
- Slowly Changing Dimensions (Type 2)
- Parquet Support
- CDC Simulation
- Event-Driven Ingestion
- Kafka Simulation
- Dockerization
- dbt Migration
- Cloud Deployment
- Dashboard Integration