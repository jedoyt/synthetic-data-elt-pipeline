import json
from datetime import datetime
from pathlib import Path

from src.transform.silver_writer import SilverWriter


def transform_customers():
    """
    Transform customer reference data
    from the Bronze layer to the Silver layer.
    """
    silver_writer = SilverWriter()

    # Source directory for bronze files
    BRONZE_DIR = Path(__file__).resolve().parents[2] / "data/bronze"
    entity = "customers"

    # Get filenames in the bronze directory for the specified entity
    bronze_entity_dir = BRONZE_DIR / entity
    bronze_filenames = [f for f in bronze_entity_dir.iterdir() if f.is_file() and f.suffix == ".jsonl"]

    # Check if there are any bronze files for the entity
    if not bronze_filenames:
        print(f"No bronze files found for entity: {entity}")
        result = {"status": "NO_BRONZE_FILES", "message": f"No bronze files found for entity: {entity}"}
        print(result)
        return result

    # Choose the latest bronze file based on the last modified timestamp
    latest_bronze_file = max(bronze_filenames, key=lambda f: f.stat().st_mtime)
    print(f"Latest bronze file for {entity}: {latest_bronze_file}")

    # Read the bronze_file and convert to list of dictionaries
    with open(latest_bronze_file, "r") as jsonl_file:
        # Transform the JSONL records to a list of dictionaries
        bronze_records = [json.loads(line) for line in jsonl_file]

    # Apply transformations and checks on every record
    staged_records = [] # Staging container for transformed data
    for record in bronze_records:
        staged_record = {}
        for key, value in record.items():
            if key == "age" and value is not None:
                try:
                    # Ensure that age is an integer and greater than 0
                    try:
                        assert int(value) > 0
                    except AssertionError as e:
                        print(f"AssertionError: {e}")
                        print(f"Age must be a positive integer for this record: {record}")
                        raise
                    staged_record[key] = int(value)
                    continue
                except Exception as e:
                    print(f"Exception: {e}")
                    print(f"Unable to convert {key} ({value}) to integer from this record:\n{record}")
                    raise

            # Create an additional data by extracting the date from registration_ts 
            # and naming the key "registration_date"
            elif key == "registration_ts" and value is not None:
                try:
                    staged_record[key] = value
                    staged_record["registration_date"] = datetime.fromisoformat(value).date()
                    continue
                except Exception as e:
                    print(f"Exception: {e}")
                    print(f"Unable to extract date from {key} ({value}) for this record: {record}")
                    raise
            
            elif value is None:
                if key in ("username", "email"):
                    try:
                        assert value is not None
                    except AssertionError as e:
                        print(f"AssertionError: {e}")
                        print(f"{key} cannot be None for this record: {record}")
                        raise
                else:
                    staged_record[key] = ""
                    continue
            else:
                staged_record[key] = value
                continue
        staged_records.append(staged_record)

    # Transform by writing the records to a CSV file in the Silver layer
    result = silver_writer.write_csv(records=staged_records, entity_name=entity)
    result["status"] = "SUCCESS"
    print(result)
    return result


# Test transform_customers
if __name__ == "__main__":
    result = transform_customers()