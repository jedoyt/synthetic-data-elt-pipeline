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
        # for row in rows:
        #     # Organize values to pass to SQL script
        #     cols = tuple(row.keys())
        #     vals = tuple(row.values()) # All values are in string format

        #     # Iterate vals to check and convert numerical data to either int or float
        #     # before INSERT INTO <table_name>
        #     vals_for_insert = [] # Placeholder for values for INSERT INTO <table_name>
        #     for val in vals:
        #         try:
        #             int(val)
        #             vals_for_insert.append(int(val))
        #         except ValueError:
        #             try:
        #                 float(val)
        #                 vals_for_insert.append(float(val))
        #             except ValueError:
        #                 if "'" in val:
        #                     vals_for_insert.append(f'"{val}"')
        #                 else:
        #                     vals_for_insert.append(f"'{val}'")

        #     sql_script = f"""
        #     INSERT INTO {table_name}
        #     ({', '.join([col for col in cols])})
        #     VALUES ({', '.join([str(val) for val in vals_for_insert])});
        #     """
        #     # print(f"SQL to execute:\n{sql_script}")
            
        #     try:
        #         self.cursor.execute(sql_script)
        #         self.connection.commit()
        #         row_count+=1
        #     except sqlite3.IntegrityError:
        #         # Row is already existing in table based on PRIMARY KEY
        #         print("UNIQUE constraint failed: dim_customers.customer_id\nContinue to next iteration")
        #         continue
            
        # print(f"{row_count} inserted to table {table_name}")
        
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
        except sqlite3.IntegrityError:
            # A row is already existing in table based on PRIMARY KEY
            print("UNIQUE constraint failed: dim_customers.customer_id\nContinue to next iteration")
            row_count = 0
        
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
    # from pprint import pprint
    manager = SQLiteManager()

    # # Path to schema.sql
    # SCHEMA_PATH = Path(__file__).resolve().parents[2] / "sql/schema.sql"

    # # Create the tables
    # manager.execute_script(SCHEMA_PATH)
    # manager.cursor.execute(
    #     "SELECT * FROM sqlite_master WHERE type='table';"
    # )
    # manager.connection.commit()
    # # Check the tables
    # for item in manager.cursor.fetchall():
    #     print(f'\n{item[0]}: {item[1]}')
    #     pprint(item[4])

    # # Access the tables
    # manager.connection = sqlite3.Row

    # Check the first few rows of table
    table_name = "dim_customers"
    sample_rows = manager.cursor.execute(
        f"SELECT * FROM {table_name} LIMIT 5;"
    ).fetchall()
    print(f"Table: {table_name}")
    for row in sample_rows:
        print(row)

    manager.close()