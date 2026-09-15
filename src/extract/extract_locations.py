import json
from datetime import UTC, datetime
from pathlib import Path

from src.extract.api_client import APIClient
from src.extract.bronze_writer import BronzeWriter
from src.metadata.metadata_manager import MetadataManager

# Open config and fetch BASE_URL
API_CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs/api_config.json"
with open(API_CONFIG_PATH) as file:
    api_config = json.load(file)
URL_PREFIX = api_config["BASE_URL"]

def extract_locations():
    """
    Extract location reference data
    from the source API and persist
    the raw payload into the Bronze layer.
    """
    client = APIClient(url_prefix=URL_PREFIX)
    writer = BronzeWriter()

    locations = client.get("/locations")

    result = writer.write_jsonl(
        records=locations["data"]["records"],
        entity_name="locations"
    )
    print("Location extraction complete!")
    print(result)
    # Save watermark to metadata file
    # The watermark is the last_extraction_ts when extraction of locations was completed, which is the current timestamp
    last_extraction_ts = datetime.now(UTC).isoformat()
    metadata_manager = MetadataManager(metadata_filename="bronze_metadata.json")
    metadata_manager.update_and_save(
        entity="locations",
        metadata_filename="bronze_metadata.json",
        set_metadata={"last_extraction_ts": last_extraction_ts}
    )
    return result


# Test extract_locations
if __name__ == "__main__":
    result = extract_locations()