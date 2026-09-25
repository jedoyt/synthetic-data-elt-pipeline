import csv
from pathlib import Path

SILVER_DIR = Path(__file__).resolve().parents[2] / "data/silver"


class SilverWriter:

    def write_csv(self, records: list, entity_name: str) -> dict:
        """
        Writes a CSV file out of the received list of records.
        Each record is a dictionary representing a row in the CSV file.
        :param records: The list of dictionaries to be written to CSV
        :param entity_name: The name of the entity to be used in the output filename
        """

        # Ensure records is a valid list
        if not isinstance(records, list):
            print("TypeError: The list of records is not a valid list")
            print("No CSV file will be written for this entity.")
            return {
                        "filepath": None,
                        "record_count": 0,
                        "message": "TypeError: The list of records is not a valid list"
                    }

        # Setup output path for CSV file
        output_filename = f"{entity_name}.csv"
        output_path = SILVER_DIR / entity_name
        output_path.mkdir(parents=True, exist_ok=True)
        output_path = output_path / output_filename

        # Write CSV file from the list of dictionaries
        with open(output_path, "w", newline='') as csv_file:
            if records:
                writer = csv.DictWriter(csv_file, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
                print("Silver CSV file written successfully!")
                return {
                    "filepath": str(output_path),
                    "record_count": len(records)
                }
            # Ensure records is not empty
            elif not records:
                print("ValueError: The list of records is empty")
                print("No CSV file will be written for this entity.")
                return {
                    "filepath": None,
                    "record_count": 0,
                    "message": "ValueError: The list of records is empty"
                }


# Test SilverWriter
# if __name__ == '__main__':
#     from pprint import pprint
#     # Source directory for bronze files
#     BRONZE_DIR = Path(__file__).resolve().parents[2] / "data/bronze"
#     entity = "customers"

#     # Get filenames in the bronze directory for the specified entity
#     bronze_entity_dir = BRONZE_DIR / entity
#     bronze_filenames = [f for f in bronze_entity_dir.iterdir() if f.is_file() and f.suffix == ".jsonl"]

#     # Initialize SilverWriter and write CSV files for each bronze JSONL file
#     silver_writer = SilverWriter()
#     for bronze_file in bronze_filenames:
#         print(f"Found bronze file: {bronze_file}")
#         # Read JSONL file and convert to list of dictionaries
#         with open(bronze_file, "r") as jsonl_file:
#             records = [json.loads(line) for line in jsonl_file]
#         result = silver_writer.write_csv(records=records, entity_name=entity)
#         print("Silver CSV file written successfully!")
#         pprint(result)  # Print the result of the CSV writing operation

