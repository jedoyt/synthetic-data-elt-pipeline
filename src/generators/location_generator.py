# Fetch random location data from locations.json and return a dictionary of the location data
import json
import random
from pathlib import Path

BASED_DIR = Path(__file__).parent
LOCATION_FILE = BASED_DIR / 'locations.json'

with open(LOCATION_FILE) as f:
    LOCATIONS = json.load(f)

def get_random_location() -> dict:
    """
    Returns a dictionary representing a randomly chosen location.
    return: A dictionary containing the location data.
    """
    return random.choice(LOCATIONS)


# Test the function
# if __name__ == "__main__":
#     print(get_random_location())