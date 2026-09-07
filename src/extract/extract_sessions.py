import json
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from src.extract.api_client import APIClient
from src.extract.bronze_writer import BronzeWriter

# Open config and fetch BASE_URL
API_CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs/api_config.json"
with open(API_CONFIG_PATH) as file:
    api_config = json.load(file)
URL_PREFIX = api_config["BASE_URL"]

client = APIClient(url_prefix=URL_PREFIX)
writer = BronzeWriter()

def extract_sessions(since_ts=None):
    """
    Extract sessions from the source API and persist
    the raw payload into the Bronze layer.
    If a timestamp is provided for since_ts, only sessions since that timestamp will be extracted.
    If no timestamp is provided, all sessions will be extracted.
    : param since_ts: str - An ISO-8601 format timestamp
    : return: a dictionary containing the filepath of the output JSONL and record counts written
    : rtype: dict
    """

    if since_ts:
        # Check since_ts is a valid ISO-8601 format timestamp
        try:
            datetime.fromisoformat(since_ts)
        except ValueError:
            raise ValueError("since_ts must be a valid ISO-8601 format timestamp, e.g., '2026-09-06 00:00:00' or '2026-09-06T00:00:00+00:00'")

        # Format the timestamp for URL encoding
        # formatted_ts = since_ts.replace(" ", "%20").replace(":", "%3A").replace("+", "%2B")
        formatted_ts = quote(since_ts, safe='')
        endpoint = f"/sessions/since/{formatted_ts}"
        sessions = client.get(endpoint)
        if sessions["data"]["record_count"]:
            result = writer.write_jsonl(
                records=sessions["data"]["records"],
                entity_name="sessions"
            )
            print(f"Sessions extraction since {since_ts} complete!")
            print(result)
            return result
        else:
            print(f"No sessions found since {since_ts}!")
            print("No bronze JSONL file was written.")
    elif since_ts is None:
        endpoint = "/sessions"
        sessions = client.get(endpoint)
        if sessions["data"]["record_count"]:
            result = writer.write_jsonl(
                records=sessions["data"]["records"],
                entity_name="sessions"
            )
            print("Full extraction of all sessions complete!")
            print(result)
            return result


# Test extract_customers
if __name__ == "__main__":
    result = extract_sessions(since_ts="2026-09-07 00:00:00")
    # result = extract_sessions()