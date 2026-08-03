# Project Charter
## Project Title
Synthetic E-Commerce ELT Pipeline using Python, SQLite, and Medallion Architecture

## Project Overview
This project aims to build an end-to-end ELT (Extract, Load, Transform) data platform that ingests synthetic e-commerce data generated from a Faker-powered pseudo REST API.

The platform will simulate a real-world e-commerce operational system and process business entities such as customers, products, orders, payments, and shipments.

Data will first be loaded into a Bronze layer in its raw form, then transformed using SQL into Silver and Gold layers stored in SQLite.

The project is designed to strengthen foundational data engineering skills using Python and SQL while applying industry-standard concepts such as Medallion Architecture, incremental loading, data quality validation, and warehouse modeling.

## Business Problem

An e-commerce company needs an analytics platform capable of transforming operational transaction data into business insights.

The company currently generates transactional data but lacks a centralized analytics environment that can:

* Track revenue trends
* Analyze customer purchasing behavior
* Measure product performance
* Monitor order fulfillment performance
* Support future analytical reporting use cases

The objective is to build a reliable ELT pipeline that converts operational data into analytics-ready datasets.

## Project Objectives
### Primary Objectives
* Build a complete ELT pipeline.
* Practice loading raw data prior to transformation.
* Develop strong SQL transformation skills.
* Implement Medallion Architecture.
* Design dimensional models for analytics.
* Implement incremental load processing.
* Create a maintainable project structure using Python and SQL.

### Secondary Objectives
* Learn data quality validation techniques.
* Practice pipeline logging and monitoring.
* Implement simple orchestration logic.
* Develop portfolio-ready engineering documentation.

## Scope

### Data Generation: Event-Producing Operational System

Synthetic REST-like service built with:

* Python
* Faker - for generating synthetic user session details
* https://www.mockaroo.com - for generating fixed tables, in case we decide to prefer it, like user locations as scope of shipment/delivery, fixed product inventory with prices, etc. All stored as a JSON file to be accessed by the python scripts of our Event-Producing Operational System

Entities:

* Customers
* Products
* Orders
* Order Items
* Payments
* Shipments

### Data Ingestion

Python extraction process that:

* Calls pseudo API endpoints
* Retrieves JSON data
* Stores raw records
* Maintains ingestion metadata

### Data Storage

Bronze:
```
JSONL Files
```

Silver:
```
SQLite
```

Gold:
```
SQLite
```

### Data Transformation

Transformations written entirely in SQL files.

No ORM-based transformations.

Examples:
```sql
SELECT
    customer_id,
    COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id;
```

### Analytics Outputs

Gold marts:

* Daily Revenue
* Customer Lifetime Value
* Product Performance
* Order Fulfillment Metrics
* Payment Method Analysis

## Out of Scope

The following are intentionally excluded:
(But expect that our python codes will resemble some of these technologies)
* Cloud platforms
* Airflow
* Docker
* Kubernetes
* Kafka
* Spark
* Snowflake
* Databricks
* dbt
* Machine Learning

These may be explored as future enhancements.

## Stakeholders
### Primary Stakeholder

Data Engineering Learner

Purpose:

* Skill development
* Portfolio development

### Secondary Stakeholder

Analytics Consumer

Consumes:

* Revenue metrics
* Customer metrics
* Product metrics

## Data Sources
### Source Type

Synthetic Operational System

### Generation Method

Python service using Faker

### Access Method

Pseudo REST API

Example endpoints:
```
GET /customers
GET /products
GET /orders
GET /payments
GET /shipments
```

### Update Frequency

Continuous synthetic generation on configurable intervals.

Example:
```
Every 10 seconds
```

## Architecture
```
Synthetic Data Generator
        │
        ▼
Pseudo REST API
        │
        ▼
Extract Layer
(Python)
        │
        ▼
Bronze Layer
(JSONL)
        │
        ▼
Load Layer
(SQLite Raw)
        │
        ▼
Silver Layer
(SQL Transformations)
        │
        ▼
Gold Layer
(SQL Analytics Models)
        │
        ▼
Business Insights
```

## Medallion Architecture
### Bronze

Purpose:

Store source data exactly as received.

Characteristics:

* Immutable
* Append-only
* Raw JSONL

Files:
```
customers.jsonl
products.jsonl
orders.jsonl
payments.jsonl
shipments.jsonl
```

But I think it is more realistic to expect the raw data to be batches of session data where every session contains multiple events where it at least contain the app_open and app_close events to signal the beginning and ending of a session.
```
events_sessions_<YYYY-MM-DDTHH:MM:SS.sssZ>.jsonl
```
We expect a unit of session data contains the following:
* session information (session_id, location, other user information)
* event timestamps (event_ts)
* customer and platform actions (the events)
    - app_open
    - product_view
    - cart_action
    - payment/purchase
    - shipment/delivery
    - app_close


### Silver

Purpose:

Create clean business entities.

Operations:

* Deduplication
* Data type casting
* Null handling
* Standardization
* Referential integrity validation

Example tables:
```
silver_customers
silver_products
silver_orders
silver_payments
silver_shipments
```

### Gold

Purpose:

Analytics-ready datasets.

Examples:
```
fact_orders
dim_customer
dim_product
```

Analytics marts:
```
gold_daily_revenue
gold_customer_ltv
gold_product_sales
gold_order_fulfillment
```

## ELT Strategy
### Extract

Retrieve records from pseudo API.

### Load

Store records into:
```
Bronze JSONL
```

and
```
Raw SQLite tables
```

without transformations.

### Transform

Execute SQL scripts against SQLite.

Example:
```
sql/
├── silver/
├── gold/
```

Transformations occur after loading.

This project follows a true ELT pattern.

## Data Quality Requirements
### Completeness

Required fields:

* customer_id
* order_id
* product_id

### Uniqueness

Unique identifiers:

* customer_id
* order_id
* payment_id
* shipment_id

### Validity

Examples:
```
quantity > 0
amount >= 0
order_date IS NOT NULL
```
### Referential Integrity

Examples:
```
order.customer_id
must exist in
customer.customer_id
```

## Incremental Loading Strategy

Approach:

Watermark-based loading.

Tracked fields:
```
created_at
updated_at
```

Metadata table:
```
pipeline_metadata
```

Stores:

* previous execution time
* latest processed timestamp
* execution status

## Success Criteria

The project is considered successful when:

✅ Synthetic data is continuously generated

✅ Data can be extracted from pseudo API endpoints

✅ Raw data is stored in Bronze JSONL files

✅ Raw data is loaded into SQLite

✅ SQL transformations create Silver datasets

✅ SQL transformations create Gold marts

✅ Incremental loading works correctly

✅ Data quality checks are implemented

✅ Pipeline execution logs are generated

✅ Full project documentation is completed

## Deliverables
### Code Deliverables
```
src/
api/
bronze/
sql/
silver/
gold/
logs/
config/
```

### Technical Deliverables
* Working ELT pipeline
* SQL transformation layer
* SQLite warehouse
* Incremental loading mechanism
* Data quality framework
* Logging framework

### Portfolio Deliverables
* Architecture Diagram
* README
* Data Dictionary
* Pipeline Flow Diagram
* Sample Analytics Queries
* Project Walkthrough Documentation

## Future Enhancements (Phase 2)

Once the foundation is complete, the project can evolve into:

* Custom Python orchestrator
* Scheduling system
* Slowly Changing Dimensions (Type 2)
* Parquet support
* CDC simulation
* Event-driven ingestion
* Kafka simulation
* Dockerization
* dbt migration
* Cloud deployment

## My One Recommended Refinement

I would add a Business Questions section because it gives purpose to every Gold model.

### Business Questions
1. What is the daily revenue trend?
2. Who are the highest-value customers?
3. Which products generate the most revenue?
4. What is the average order value?
5. Which payment methods are most frequently used?
6. What percentage of orders are delivered on time?
7. Which customers are repeat buyers?
8. Which product categories drive the most sales?

This section will later drive your Gold-layer design and make the project feel like a real analytics platform instead of a purely technical exercise.