import json
from pathlib import Path

from src.generators.session_generator import generate_session

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "sample_output"
OUTPUT_FILE = OUTPUT_DIR / "sessions_batch.json"

def classify_session(session: dict) -> dict:
    event_types = [event["event_type"] for event in session["events"]]
    if "purchase" in event_types:
        return "purchase"
    if "cart_action" in event_types:
        return "abandoned_cart"
    else:
        return "browse_only"

def generate_batch(num_of_sessions: int, save_json: bool = False):
    """Generate a batch of sessions and optionally save it as JSON."""
    if not isinstance(num_of_sessions, int) or isinstance(num_of_sessions, bool):
        raise TypeError("num_of_sessions must be an integer")
    if num_of_sessions < 0:
        raise ValueError("num_of_sessions must be non-negative")

    print(f"Generating batch of {num_of_sessions} sessions...")

    sessions = [generate_session() for _ in range(num_of_sessions)]

    summary = {
        "total_sessions": len(sessions),
        "browse_only": 0,
        "abandoned_cart": 0,
        "purchase": 0,
        "total_events": 0,
    }

    for session in sessions:
        outcome = classify_session(session)
        summary[outcome] += 1
        summary["total_events"] += len(session["events"])

    if save_json:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Saving at {OUTPUT_FILE}...")
        with open(OUTPUT_FILE, 'w', encoding="utf-8") as file:
            json.dump(sessions, file, indent=4)

    # Percent distributions
    browse_only = round(100 * summary['browse_only'] / summary['total_sessions'], 0)
    abandoned_carts = round(100 * summary['abandoned_cart'] / summary['total_sessions'], 0)
    purchases = round(100 * summary['purchase'] / summary['total_sessions'], 0)

    # Batch summary report
    print("Batch generation complete")
    print(f"Total sessions: {summary['total_sessions']}")
    print(f"Browse-only sessions ({browse_only}%): {summary['browse_only']}")
    print(f"Abandoned-cart sessions ({abandoned_carts}%): {summary['abandoned_cart']}")
    print(f"Purchase sessions ({purchases}%): {summary['purchase']}")
    print(f"Total events: {summary['total_events']}")

    if save_json:
        print(f"Saved output to: {OUTPUT_FILE}")

    return sessions

# Run batch generation
if __name__ == "__main__":
    generate_batch(25, True)
