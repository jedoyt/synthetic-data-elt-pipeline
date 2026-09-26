PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id INTEGER PRIMARY KEY,
    registration_ts TEXT,
    registration_date TEXT,
    username TEXT,
    email TEXT,
    gender TEXT,
    age INTEGER,
    nationality TEXT
);

CREATE TABLE IF NOT EXISTS dim_products (
    product_id INTEGER PRIMARY KEY,
    category TEXT,
    sub_category TEXT,
    product_name TEXT,
    price REAL,
    url TEXT
);

CREATE TABLE IF NOT EXISTS dim_locations (
    location_id INTEGER PRIMARY KEY,
    city TEXT,
    country TEXT,
    latitude REAL,
    longitude REAL
);

CREATE TABLE IF NOT EXISTS dim_sessions (
    session_id TEXT PRIMARY KEY,
    customer_id INTEGER,
    location_id INTEGER,
    device_type TEXT,
    platform TEXT,
    session_start_ts, TEXT,

    FOREIGN KEY (customer_id)
        REFERENCES dim_customers(customer_id),

    FOREIGN KEY (location_id)
        REFERENCES dim_locations(location_id)
);

CREATE TABLE IF NOT EXISTS fact_session_events (
    event_id TEXT PRIMARY KEY,

    event_sequence INTEGER,

    event_type TEXT,
    event_ts TEXT,
    attributes TEXT,

    session_id TEXT,
    customer_id TEXT,
    location_id TEXT,

    FOREIGN KEY (session_id)
        REFERENCES dim_session(session_id),
    FOREIGN KEY (customer_id)
        REFERENCES dim_customers(customer_id),
    FOREIGN KEY (location_id)
        REFERENCES dim_locations(location_id)
)