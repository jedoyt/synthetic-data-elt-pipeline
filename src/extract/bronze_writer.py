import json
from datetime import UTC, datetime
from pathlib import Path

BRONZE_DIR = Path(__file__).resolve().parents[2] / "data/bronze"


class BronzeWriter:

    def write_jsonl(self, records, entity_name: str) -> str:
        """
        Writes a JSONL file out of the received data assigned in `records` parameter
        """

        # Ensure records is either a Python list or a Python dictionary
        if not isinstance(records, (list, dict)):
            raise TypeError

        # Format timestamp suffix for JSONL filename
        timestamp_suffix = datetime.strftime(datetime.now(UTC), "%Y%m%d_%H%M%S")

        # Setup output path for JSONL file
        output_filename = f"{entity_name}_{timestamp_suffix}.jsonl"
        output_path = BRONZE_DIR / entity_name
        output_path.mkdir(parents=True, exist_ok=True)
        output_path = output_path / output_filename

        # Write JSONL file
        if isinstance(records, dict):
            records = [records]
        with open(output_path, "w") as f:
            f.writelines(json.dumps(record_dict) + '\n' for record_dict in records)
        return {
            "filepath": output_path,
            "record_count": len(records)
        }


# Test BronzeWriter
# if __name__ == '__main__':
#     # Load some sample JSON files
#     from src.generators.customer_generator import CUSTOMERS
#     from src.generators.location_generator import LOCATIONS
#     from src.generators.product_generator import PRODUCTS

#     sample_batch_path = Path(__file__).resolve().parents[1] / "generators/sample_output/sessions_batch.json"
#     with open(sample_batch_path, encoding='utf-8') as json_file:
#         sessions_batch = json.load(json_file)

#     writer = BronzeWriter()
#     records_dict = {
#         'products': PRODUCTS,
#         'customers': CUSTOMERS,
#         'locations': LOCATIONS,
#         'sessions': sessions_batch,
#     }
#     for entity_name, records in records_dict.items():
#         path = writer.write_jsonl(records=records, entity_name=entity_name)
#         print(f"JSONL file written successfully!\n{path}")