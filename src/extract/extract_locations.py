import json
from pathlib import Path

from src.extract.api_client import APIClient
from src.extract.bronze_writer import BronzeWriter

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
        records=locations["data"],
        entity_name="locations"
    )
    print("Location extraction complete!")
    print(result)
    return result


# Test extract_customers
if __name__ == "__main__":
    result = extract_locations()