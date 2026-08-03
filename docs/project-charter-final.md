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
FROM silver_orde*s
GROUP BY customer_id;
```

---

*# Analytics Outputs

Gold marts wi*l support:

- Revenue Analysis
- C*stomer Lifetime Value
- Customer C*nversion Analysis
- Product Perfor*ance Analysis
- Session Analytics
* Cart Abandonment Analysis
- Order*Fulfillment Analysis
- Payment Met*od Analysis

---

# Out of Scope

*he following technologies are inte*tionally excluded from the initial*implementation:

- Cloud Platforms*- Airflow
- Docker
- Kubernetes
- *afka
- Spark
- Snowflake
- Databri*ks
- dbt
- Machine Learning

Some *mplementation patterns may resembl* these technologies for learning p*rposes.

These technologies may be*explored in future project phases.*
---

# Stakeholders

## Primary S*akeholder

Data Engineering Learne*

Purpose:

- Skill development
- *ortfolio development

## Secondary*Stakeholder

Analytics Consumers

*onsumes:

- Revenue metrics
- Cust*mer metrics
- Product metrics
- Be*avioral analytics
- Operational an*lytics

---

# Data Sources

## So*rce Type

Synthetic Event-Producin* Operational System

## Generation*Method

Python service using Faker*and optional Mockaroo reference da*asets.

---

## Access Method

Pse*do REST API

Example endpoints:

`*`http
GET /sessions
GET /events
GE* /customers
GET /products
GET /ord*rs
GET /payments
GET /shipments
``*

---

## Update Frequency

Contin*ous synthetic generation at config*rable intervals.

Example:

```tex*
Every 10 seconds
```

---

# Arch*tecture

```text
Event-Producing O*erational System
                │*                ▼
        Pseudo R*ST API
                │
         *      ▼
         Extract Layer
   *        (Python)
                │*                ▼
          Bronze*Layer
        (Raw JSONL Events)
 *              │
                ▼
*         Raw SQLite
              * │
                ▼
          Sil*er Layer
      (SQL Transformation*)
                │
              * ▼
           Gold Layer
       (A*alytics Marts)
                │
 *              ▼
        Business I*sights
```

---

# Medallion Archi*ecture

## Bronze Layer

### Purpo*e

Store source data exactly as re*eived.

### Characteristics

- Imm*table
- Append-only
- Event-based
* Session-oriented
- Raw JSONL

###*Example Files

```text
events_sess*ons_2026-08-03T10-00-00Z.jsonl
eve*ts_sessions_2026-08-03T10-10-00Z.j*onl
events_sessions_2026-08-03T10-*0-00Z.jsonl
```

### Session Struc*ure

Each session may contain:

- *ession_id
- customer_id
- location*- device information
- event times*amps
- customer actions

### Suppo*ted Events

- app_open
- product_v*ew
- cart_action
- payment
- purch*se
- shipment_update
- delivery_co*firmation
- app_close

No transfor*ations are performed in Bronze.

-*-

## Silver Layer

### Purpose

C*nvert raw event data into clean bu*iness entities and standardized ev*nt models.

### Operations

- Dedu*lication
- Data type casting
- Nul* handling
- Standardization
- Refe*ential integrity validation
- Even* normalization
- Session reconstru*tion

### Example Tables

```text
*ilver_sessions
silver_events
silve*_customers
silver_products
silver_*rders
silver_payments
silver_shipm*nts
```

Silver represents the ope*ational business view.

---

## Go*d Layer

### Purpose

Provide anal*tics-ready models designed to answ*r business questions.

### Dimensi*nal Models

```text
fact_orders
fa*t_sessions
fact_payments

dim_cust*mer
dim_product
dim_location
dim_d*te
```

### Analytics Marts

```te*t
gold_daily_revenue
gold_customer*ltv
gold_repeat_customers
gold_pro*uct_performance
gold_conversion_fu*nel
gold_cart_abandonment
gold_ses*ion_metrics
gold_order_fulfillment*```

Gold represents the analytica* business view.

---

# ELT Strate*y

## Extract

Retrieve data from *seudo API endpoints.

---

## Load*
Store records into:

- Bronze JSO*L files
- Raw SQLite tables

witho*t modification.

---

## Transform*
Execute SQL scripts against SQLit*.

```text
sql/
├── raw/
├── silve*/
├── gold/
```

All transformatio*s occur after data loading.

This *roject follows a true ELT architec*ure.

---

# Data Quality Requirem*nts

## Completeness

Required fie*ds include:

- session_id
- custom*r_id
- event_ts
- event_type

---
*## Uniqueness

Unique identifiers *nclude:

- session_id
- customer_i*
- order_id
- payment_id
- shipmen*_id

---

## Validity

Examples:

*``sql
quantity > 0
amount >= 0
eve*t_ts IS NOT NULL
event_type IS NOT*NULL
```

---

## Referential Inte*rity

Examples:

```text
order.cus*omer_id
must exist in
customer.cus*omer_id
```

```text
event.session*id
must exist in
session.session_i*
```

---

# Incremental Loading S*rategy

## Approach

Watermark-bas*d loading.

### Tracked Fields

``*text
created_at
updated_at
event_t*
```

### Metadata Table

```text
*ipeline_metadata
```

Stores:

- P*evious execution time
- Latest pro*essed timestamp
- Execution status*- Rows extracted
- Rows loaded
- R*ws transformed

---

# Business Qu*stions

The Gold layer should answ*r the following questions:

### Re*enue & Sales

- What is the daily *evenue trend?
- What is the averag* order value?
- Which products gen*rate the most revenue?

### Custom*r Analytics

- Who are the highest*value customers?
- Which customers*are repeat buyers?
- What is the c*stomer lifetime value?

### Produc* Analytics

- Which products are m*st viewed?
- Which products are mo*t purchased?
- Which product categ*ries drive the most sales?

### Cu*tomer Journey Analytics

- How man* sessions result in purchases?
- W*at is the purchase conversion rate*
- Where do customers drop off in *he funnel?
- Which products are fr*quently abandoned in carts?

### O*erational Analytics

- What percen*age of orders are delivered on tim*?
- Which payment methods are most*frequently used?

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