import json
from pathlib import Path

from src.extract.api_client import APIClient
from src.extract.bronze_writer import BronzeWriter

# Open config and fetch BASE_URL
API_CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs/api_config.json"
with open(API_CONFIG_PATH) as file:
    api_config = json.load(file)
URL_PREFIX = api_config["BASE_URL"]

def extract_sessions(since_ts=None):
    """
    Extract sessions from the source API and persist
    the raw payload into the Bronze layer.
    : param since_ts, str - An ISO-8601 format timestamp
    : return: a dictionary containing the filepath of the output JSONL and record counts written
    : rtype: dict
    """
    client = APIClient(url_prefix=URL_PREFIX)
    writer = BronzeWriter()

    if since_ts:
        formatted_ts = since_ts.replace(" ", "%20").replace(":", "%3A").replace("+", "%2B")

        sessions = client.get(f"/sessions/since/{formatted_ts}")
        if sessions["data"]["session_count"]:
            result = writer.write_jsonl(
                records=sessions["data"]["sessions"],
                entity_name="sessions"
            )
            print(f"Sessions extraction since {since_ts} complete!")
            print(result)
            return result
        else:
            print(f"No sessions found since {since_ts}!")


# Test extract_customers
if __name__ == "__main__":
    result = extract_sessions(since_ts="2026-08-29 14:00:00")