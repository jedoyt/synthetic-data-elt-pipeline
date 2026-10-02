import csv
from pathlib import Path

# Path to schema.sql
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "sql/schema.sql"

# Source Silver Path
SILVER_PATH = Path(__file__).resolve().parents[2] / "data/silver"

def check_or_create_tables(sqlite_manager, schema_file=None):
    """
    Check for existence of database tables.
    If schema_file is provided, create the database tables as
    defined by the schema from SQL script file
    """

    if schema_file:
       sqlite_manager.execute_script(SCHEMA_PATH)
       print("Creating database tables...")
    
    sqlite_manager.cursor.execute(
        "SELECT * FROM sqlite_master WHERE type='table';"
    )
    sqlite_manager.connection.commit()
    if schema_file is None:
        print("Checking existing database tables...")
    for i, item in enumerate(sqlite_manager.cursor.fetchall(), start=1):
        print(f'{item[0]} {i}: {item[1]}')
    print("SQL script executed successfully!\n")

def load_csv(csv_path) -> list[dict]:
    with open(csv_path, newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)

def load_csv_to_table(csv_path, table_name, sqlite_manager):
    print(f"Loading data to table {table_name}...")
    print(f"Silver source: {csv_path}")
    rows = load_csv(csv_path)
    results = sqlite_manager.insert_rows(table_name, rows)
    if results['record_count']:
        results['status']= 'SUCCESS'
    print(results)
    return results

# Test load_csv_to_table
# if __name__ == '__main__':
#     from src.load.sqlite_manager import SQLiteManager
#     sqlite_manager = SQLiteManager()
#
#     ENTITY_TABLE_MAP = {
#         "customers": "dim_customers",
#         "products": "dim_products",
#         "locations": "dim_locations",
#         "sessions": "dim_sessions",
#         "session_events": "fact_session_events",
#     }
#
#     # # Insert rows
#     # for entity, table_name in ENTITY_TABLE_MAP.items():
#     #     csv_path = SILVER_PATH / f"{entity}/{entity}.csv"
#     #     result = load_csv_to_table(csv_path, table_name, sqlite_manager)
#     #     print(result)

#     # # Drop Tables
#     # for table_name in ENTITY_TABLE_MAP.values():
#     #     drop_result = sqlite_manager.drop(table_name)
#     #     print(drop_result)

#     # # Create Tables
#     # check_or_create_tables(SCHEMA_PATH)
