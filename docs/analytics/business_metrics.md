# Business Metrics

## Key Performance Indicators (KPI)
### KPI 1: Total Purchases
**"How many purchases were completed?"**

This is the most basic revenue-related metric

Query:
```sql
SELECT
    COUNT(*) AS total_purchases
FROM fact_session_events
WHERE event_type = 'purchase';
```

#### SQL Logic

##### Step 1:

`SELECT` the `fact_session_events` table

Event Types: `app_open`, `product_view`, `cart_action`, `purchase`, `app_close`
(Note: 1 row represents 1 event)

##### Step 2:

Use `WHERE` to filter by `event_type`

##### Step 3:

Use `COUNT(*)` to count the rows

Example Output:
```shell
% python -m src.load.sqlite_manager
Connected to database sucessfully!
Database filepath: /.../synthetic-data-elt-pipeline/data/gold/analytics.db

total_purchases
---------------
13             
Database connection closed!
```

#### Business Interpretation

18 completed purchases occurred

within the analyzed dataset.

### KPI 2: Purchase Conversion Rate
**What percentage of sessions resulted in a purchase?**

This is significantly more useful than total purchases.

Full Query:
```sql
SELECT
    ROUND(
        COUNT(
            DISTINCT CASE
                WHEN event_type='purchase'
                THEN session_id
            END
        ) * 100.0 / COUNT(DISTINCT session_id),
        2
    ) AS purchase_conversion_rate
FROM fact_session_events;
```

#### SQL Logic
##### Denominator
Count total sessions-- 100 sessions.

##### Numerator
Count session containing at least one `"purchase"`.

##### Formula: (`purchase_sessions` / `total_sessions`) * 100

Example Output:
```shell
% python -m src.load.sqlite_manager
Connected to database sucessfully!
Database filepath: /.../synthetic-data-elt-pipeline/data/gold/analytics.db

purchase_conversion_rate
------------------------
13.0                    
Database connection closed!
```
#### Business Interpretation
13% of all sessions ended with a successful purchase.

### KPI 3: Cart Abandonment Rate
**How many users added items to the cart but never purchased?**

A classic conversion funnel metric

Full Query:
```sql
SELECT
    ROUND(
        (
            COUNT(
                DISTINCT CASE
                    WHEN event_type='cart_action'
                    THEN session_id
                END
            )
            -
            COUNT(
                DISTINCT CASE
                    WHEN event_type='purchase'
                    THEN session_id
                END
            )
        ) * 100.0
        /
        COUNT(
            DISTINCT CASE
                WHEN event_type='cart_action'
                THEN session_id
            END
        ),
        2
    ) AS cart_abandonment_rate
FROM fact_session_events;
```

#### SQL Logic
Suppose we have 40 sessions with "cart_actions" and 25 session with "purchases".
Then abandoned session is 40 - 25 = 15. Abandonment rate is 15 / 40 * 100 = 37.5%

Example Output:
```shell
% python -m src.load.sqlite_manager
Connected to database sucessfully!
Database filepath: /.../synthetic-data-elt-pipeline/data/gold/analytics.db

cart_abandonment_rate
---------------------
37.50                
Database connection closed!
```

#### Business Interpretation
37.5% of sessions that interacted with the cart never completed a purchase.

A high value here indicates the following:
* Checkout friction
* Poor pricing
* User hesitation
* Payment issues

### KPI 4: Average Events Per Session
**How engaged is the average customer session?**

Full Query:
```sql
SELECT
    ROUND(
        COUNT(*) * 1.0
        /
        COUNT(DISTINCT session_id),
        2
    ) AS avg_events_per_session
FROM fact_session_events;
```

#### SQL Logic
Suppose we have 605 event from these 100 sessions, we'll just divide 605 by 100 to get the average events per session.

#### Business Interpretation
The average sessionm, therefore, contains 6.05 interactions.

Example Output:
```shell
% python -m src.load.sqlite_manager
Connected to database sucessfully!
Database filepath: /.../synthetic-data-elt-pipeline/data/gold/analytics.db

avg_events_per_session
----------------------
6.05                  
Database connection closed!
```

### KPI 5: Sessions By Platform
**Which platform is most used?**

Full Query:
```sql
SELECT
    platform,
    COUNT(*) AS total_sessions
FROM dim_sessions
GROUP BY platform
ORDER BY total_sessions DESC;
```

#### SQL Logic
Use the `GROUP BY` to group the query by platform. This also requires an aggregation, in this case `COUNT(*) AS total_sessions`.

Example Output:
```shell
% python -m src.load.sqlite_manager
Connected to database sucessfully!
Database filepath: /.../synthetic-data-elt-pipeline/data/gold/analytics.db

platform | total_sessions
---------+---------------
linux    | 28            
android  | 25            
ios      | 21            
windows  | 15            
macos    | 11            
Database connection closed!
```

### KPI 6: Sessions By Country
**Which countries generate the most activity?**

Full Query:
```sql
SELECT
    dl.country,
    COUNT(*) AS total_sessions
FROM dim_sessions ds
JOIN dim_locations dl
    ON ds.location_id =
       dl.location_id
GROUP BY dl.country
ORDER BY total_sessions DESC;
```
#### SQL Logic
A session doesn't directly contain country information so we need to `JOIN` `dim_sessions` `ON` `dim_locations`.

Example Output:
```shell
% python -m src.load.sqlite_manager
Connected to database sucessfully!
Database filepath: /.../synthetic-data-elt-pipeline/data/gold/analytics.db

country               | total_sessions
----------------------+---------------
Indonesia             | 12            
China                 | 12            
United States         | 6             
Russia                | 5             
Philippines           | 5             
Thailand              | 4             
Sweden                | 4             
Poland                | 3             
Peru                  | 3             
Mexico                | 3             
Japan                 | 3             
Brazil                | 3             
Yemen                 | 2             
Portugal              | 2             
Palestinian Territory | 2             
Kazakhstan            | 2             
Iran                  | 2             
Germany               | 2             
Canada                | 2             
South Korea           | 1             
South Africa          | 1             
Slovenia              | 1             
Serbia                | 1             
Panama                | 1             
Norway                | 1             
New Zealand           | 1             
Netherlands           | 1             
Mauritania            | 1             
Lithuania             | 1             
Kiribati              | 1             
Italy                 | 1             
Israel                | 1             
France                | 1             
Finland               | 1             
Ecuador               | 1             
Czech Republic        | 1             
Croatia               | 1             
Colombia              | 1             
Chile                 | 1             
Bolivia               | 1             
Belarus               | 1             
Albania               | 1             
Database connection closed!
```

#### Business Interpretation
This output of this query tells you the following:
* Top geographic markets
* Most active regions
* Potential growth opportunities

### KPI 7: Top Customers by Activity
**Who are the most active customers?**

Full Query:
```sql
SELECT
    customer_id,
    COUNT(*) AS total_events
FROM fact_session_events
GROUP BY customer_id
ORDER BY total_events DESC
LIMIT 10;
```
#### SQL Logic
Count events generated by each customer but `LIMIT` the rows to just 10.

#### Business Interpretation
These users represent:
* Power users
* Frequent shoppers
* Highly engaged customers

Often useful for:
* Loyalty campaigns
* Customer segmentation
* Retention analysis

Example Output:
```shell
% python -m src.load.sqlite_manager
Connected to database sucessfully!
Database filepath: /.../synthetic-data-elt-pipeline/data/gold/analytics.db

customer_id | total_events
------------+-------------
458         | 20          
765         | 16          
923         | 14          
860         | 14          
222         | 13          
395         | 12          
292         | 12          
939         | 11          
604         | 10          
47          | 10          
Database connection closed!
```

## What These KPIs Actually Form
### Funnel Metrics
If you step back, these metrics map neatly into a business funnel:
```
Sessions
    ↓
Average Events
    ↓
Product Interaction
    ↓
Cart Interaction
    ↓
Purchase
    ↓
Conversion Rate
    ↓
Abandonment Rate
```

They aren't random SQL exercises.

Together they tell the story of a customer journey within this synthetic e-commerce platform.
```
Traffic
    ↓
Engagement
    ↓
Intent
    ↓
Purchase
```

And that's exactly the type of analytical thinking that turns a warehouse into something that generates business value.