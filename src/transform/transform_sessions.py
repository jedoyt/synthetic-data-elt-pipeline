import json
from pathlib import Path

from src.transform.silver_writer import SilverWriter


def transform_sessions():
    """
    Transform session reference data
    from the Bronze layer to the Silver layer.
    """
    silver_writer = SilverWriter()
    
    # Source directory for bronze files
    BRONZE_DIR = Path(__file__).resolve().parents[2] / "data/bronze"
    entity = "sessions"
    
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
    staged_sessions = [] # Staging container for transformed sessions data
    staged_events = [] # Staging container for transformed events data
    for session_record in bronze_records:
        staged_session = {}
        for session_key, session_value in session_record.items():
            if session_key != "events":
                staged_session[session_key] = session_value
                continue
            elif session_key == "events":
                if not isinstance(session_value, list):
                    raise TypeError(f"Expected 'events' to be a list, but got {type(session_value).__name__} for this record:\n{session_record}")
                for sequence, event in enumerate(session_value, start=1):
                    staged_event = {}
                    for event_key, event_value in event.items():
                        # if event_key is "attributes", serialize as a JSON string
                        if event_key == "attributes":
                            if not isinstance(event_value, dict):
                                raise TypeError(f"Expected 'attributes' to be a dict, but got {type(event_value).__name__} for this event:\n{event}")
                            staged_event[event_key] = json.dumps(event_value)
                        # For all other event keys, just copy the value
                        else:
                            staged_event[event_key] = event_value
                    # Insert session_id, customer_id, location_id, and event_sequence into each event record
                    staged_event.update({
                        'event_sequence': sequence,
                        'session_id': staged_session.get('session_id'),
                        'customer_id': staged_session.get('customer_id'),
                        'location_id': staged_session.get('location_id'),
                    })
                    staged_events.append(staged_event)
        staged_sessions.append(staged_session)

    # Transform session records by writing staged_sessions to a CSV file in the Silver layer
    result_sessions = silver_writer.write_csv(records=staged_sessions, entity_name=entity)
    result_sessions["status"] = "SUCCESS"
    # Transform event records by writing staged_events to a CSV file in the Silver layer
    result_events = silver_writer.write_csv(records=staged_events, entity_name="session_events")
    result_events["status"] = "SUCCESS"
    print(result_sessions)
    print(result_events)

    return result_sessions, result_events

# Test transform_sessions
if __name__ == "__main__":
    transform_sessions()