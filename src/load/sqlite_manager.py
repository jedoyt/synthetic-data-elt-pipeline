import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data/gold/analytics.db"

class SQLiteManager:
    def __init__(self):
        # Open DB
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
        print(f"Connected to database sucessfully!\nDatabase filepath: {DB_PATH}")

    def execute_script(self, sql_file):
        # Execute SQL
        with open(sql_file, "r") as file:
            self.cursor.executescript(file.read())

        self.connection.commit()
        print(f"SQL script executed successfully!\nSQL source: {sql_file}")

    def insert_rows(self, table_name: str, rows: list[dict]) -> dict:
        row_count = 0
        columns = list(rows[0].keys())
        placeholders = ", ".join(["?"] * len(columns))
            
        sql = f"""
            INSERT INTO {table_name}
            ({", ".join(columns)})
            VALUES ({placeholders})
            """

        try:
            tuple_rows = [tuple(row.values()) for row in rows]
            self.cursor.executemany(sql, tuple_rows)
            self.connection.commit()
            row_count += len(tuple_rows)
        except sqlite3.IntegrityError as exc:
            # A row may already be existing in table based on PRIMARY KEY
            print(f"IntegrityError loading\n{table_name}: {exc}")
            row_count = 0
        print(f"{row_count} inserted to table {table_name}")
        return {
            "filepath": DB_PATH,
            "table_name": table_name,
            "record_count": row_count,
        }

    def drop(self, table_name) -> dict:
        self.cursor.execute(f'DROP TABLE IF EXISTS {table_name};')
        self.connection.commit()
        return {
            "filepath": DB_PATH,
            "table_name": table_name,
            "record_count": None,
            "message": f"Table {table_name} dropped from database!"
        }

    def close(self):
        # Close DB
        self.connection.close()
        print("Database connection closed!")


# Test SQLiteManager
if __name__ == "__main__":
    from pprint import pprint
    manager = SQLiteManager()

    # Path to schema.sql
    SCRIPT_PATH = Path(__file__).resolve().parents[2] / "sql/test_queries.sql"

    # Execute SQL
    sql = "SELECT * FROM fact_session_events LIMIT 5;"

    output_rows = manager.cursor.execute(sql).fetchall()
    for row in output_rows:
        print(row)


    manager.close()