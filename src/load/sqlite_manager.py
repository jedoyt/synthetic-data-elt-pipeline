import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data/gold/analytics.db"

class SQLiteManager():
    def __init__(self):
        # Open DB
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
        print(f"Connected to database sucessfully!\nDatabase filepath: {DB_PATH}")

    def set_to_sqliterow(self):
        self.connection.row_factory = sqlite3.Row

    def execute_script(self, sql_file):
        # Execute SQL
        with open(sql_file, "r") as file:
            self.cursor.executescript(file.read())

        self.connection.commit()
        print(f"SQL script executed successfully!\nSQL source: {sql_file}")

    def close(self):
        # Close DB
        self.connection.close()
        print("Database connection closed!")


# Test SQLiteManager
if __name__ == "__main__":
    manager = SQLiteManager()

    # Path to schema.sql
    SCHEMA_PATH = Path(__file__).resolve().parents[2] / "sql/schema.sql"

    manager.execute_script(SCHEMA_PATH)
    manager.set_to_sqliterow()
    tables = {
        "dim_customers": "customer_id", 
        "dim_products": "product_id", 
        "dim_locations": "location_id", 
        "dim_sessions": "session_id", 
        "fact_session_events": "event_id"
    }
    for table, primary_key in tables.items():
        manager.cursor.executescript(f"SELECT {primary_key} FROM {table};")
        row = manager.cursor.fetchone()
        print(f"{table} table exists!")

    manager.close()