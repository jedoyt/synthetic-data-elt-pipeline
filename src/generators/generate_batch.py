import json
from pathlib import Path

from session_generator import generate_session


def generate_batch(num_of_sessions, save_json=False):
    """Generate a batch of sessions and optionally save it as JSON."""
    if not isinstance(num_of_sessions, int) or isinstance(num_of_sessions, bool):
        raise TypeError("num_of_sessions must be an integer")
    if num_of_sessions < 0:
        raise ValueError("num_of_sessions must be non-negative")

    print(f"Generating batch of {num_of_sessions} sessions...")
    batch = []
    for _ in range(num_of_sessions):
        batch.append(generate_session())

    if save_json:
        BASED_DIR = Path(__file__).parent
        CUSTOMER_FILE = BASED_DIR / 'sessions_batch.json'
        print(f"Saving at {CUSTOMER_FILE}...")
        with open(CUSTOMER_FILE, 'w') as file:
            json.dump(batch, file, indent=4)
            print("Saved as batch as sessions_batch.json!")

    return batch

# Run batch generation
if __name__ == "__main__":
    generate_batch(20, True)
