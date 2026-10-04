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

    def execute_and_tabulate(self, query, params=None):
        """
        Executes a SQL query and prints out a neatly formatted table.
        """
        if params is None:
            params = ()
            
        # 1. Execute the query
        self.cursor.execute(query, params)
        
        # 2. Extract column headers from cursor description
        if not self.cursor.description:
            print("Query executed successfully (No results to display).")
            return
            
        headers = [desc[0] for desc in self.cursor.description]
        rows = self.cursor.fetchall()
        
        # 3. Dynamically calculate the maximum width for each column
        col_widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(val if val is not None else "NULL")))
                
        # 4. Generate format strings for clean grid alignments
        format_template = " | ".join(f"{{:<{w}}}" for w in col_widths)
        separator = "-+-".join("-" * w for w in col_widths)
        
        # 5. Print the table
        print()
        print(format_template.format(*headers))
        print(separator)
        for row in rows:
            # Convert None to readable 'NULL' strings
            stringified_row = [str(val) if val is not None else "NULL" for val in row]
            print(format_template.format(*stringified_row))    

    def close(self):
        # Close DB
        self.connection.close()
        print("Database connection closed!")


# Test SQLiteManager
if __name__ == "__main__":
    manager = SQLiteManager()

    # Execute and Tabulate SQL
    sql = """
        SELECT event_id, event_sequence AS seq, event_type, session_id
        FROM fact_session_events
        LIMIT 15;
        """
    manager.execute_and_tabulate(sql)

    manager.close()