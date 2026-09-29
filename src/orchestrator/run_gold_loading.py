from src.load.load_gold import (
    SCHEMA_PATH,
    SILVER_PATH,
    check_or_create_tables,
    load_csv_to_table,
)
from src.load.sqlite_manager import SQLiteManager


def run_gold_loading():
    sqlite_manager = SQLiteManager()

    ENTITY_TABLE_MAP = {
        "customers": "dim_customers",
        "products": "dim_products",
        "locations": "dim_locations",
        "sessions": "dim_sessions",
        "session_events": "fact_session_events",
    }

    results = {}

    # Insert the rows from the csv tables from data/silver for all entities
    for entity, table_name in ENTITY_TABLE_MAP.items():
        csv_path = SILVER_PATH / f"{entity}/{entity}.csv"
        result = load_csv_to_table(csv_path, table_name, sqlite_manager)
        results[table_name] = result
    return results

def print_summary(results: dict):
    """
    Print a summary of the Gold loading process.
    : param results: dict - A dictionary containing the results of the transformation process for each entity.
    """
    summary_title = "\nGold Loading Summary (analytics.db):"
    total_records = sum(result['record_count'] for result in results.values() if result)
    print("_" * len(summary_title))
    print(summary_title)
    print("=" * len(summary_title))
    for table_name, result in results.items():
        print(f"{table_name}: {result['record_count']} records")
    print("_" * len(summary_title))
    print(f"TOTAL RECORDS: {total_records}")
    print("=" * len(summary_title))    

if __name__ == "__main__":
    sqlite_manager = SQLiteManager()

    # Create the database tables
    check_or_create_tables(sqlite_manager=sqlite_manager, schema_file=SCHEMA_PATH)

    # Insert the rows from the csv tables from data/silver for all entities
    db_loading_results = run_gold_loading()
    print_summary(db_loading_results)

    sqlite_manager.close()