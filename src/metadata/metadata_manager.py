
import json
from pathlib import Path
from pprint import pprint

METADATA_FILE_PATH = Path(__file__).resolve().parent


class MetadataManager:
    """
    Class to manage metadata for different entities.
    This class provides methods to load metadata from a JSON file, update metadata for specific entities, 
    and save the updated metadata back to the file.
    """
    def __init__(self, metadata_filename: str = ""):
        self.loaded_metadata = {}
        if metadata_filename:
            self.load_metadata(METADATA_FILE_PATH / metadata_filename)

    def load_metadata(self, metadata_filename: str):
        """
        Fetch from json file the metadata for the given entity and assign it to self.loaded_metadata.
        : param metadata_file_path: str - The path to the JSON file containing metadata whose primary keys are the entity names.
        """
        with open(METADATA_FILE_PATH / metadata_filename, "r") as file:
            self.loaded_metadata = json.load(file)
            print(f"Metadata loaded from {metadata_filename}:")
            pprint(self.loaded_metadata)

    def update_and_save(self, entity: str, metadata_filename: str, set_metadata: dict):
        """
        Save the metadata for the given entity to a JSON file.
        : param entity: str - The name of the entity for which to save metadata.
        : param metadata_filename: str - The name of the JSON file where metadata should be saved.
        : param set_metadata: dict - A dictionary containing the metadata to save for the entity.
        """
        # If now metadata is loaded, raise an error and tell to load it from the file first
        if not self.loaded_metadata:
            raise ValueError("Metadata is not loaded. Please load metadata before saving.")
        # Overwrite the file with the updated metadata with proper indentation and formatting
        if self.loaded_metadata:
            self.loaded_metadata.update({entity: set_metadata})
            with open(METADATA_FILE_PATH / metadata_filename, "w") as file:
                json.dump(self.loaded_metadata, file, indent=2, sort_keys=True)
                print(f"Metadata for '{entity}' updated and saved to {metadata_filename}:")
                pprint(self.loaded_metadata)

    def get_metadata(self, entity: str) -> dict:
        """
        Get the metadata for the given entity.
        : param entity: str - The name of the entity for which to get metadata.
        : return: dict - A dictionary containing the metadata for the entity.
        """
        if not self.loaded_metadata:
            raise ValueError("Metadata is not loaded. Please load metadata before getting it.")
        if entity not in self.loaded_metadata:
            raise ValueError(f"Metadata for entity '{entity}' is not available.")
        return self.loaded_metadata.get(entity, {})


# Test MetadataManager by loading bronze_metadata.json, updating the last_extraction_ts for sessions, and saving it back to the file
if __name__ == "__main__":
    metadata_manager = MetadataManager()
    metadata_manager.load_metadata(metadata_filename="bronze_metadata.json")

    # Update the last_extraction_ts for sessions
    new_last_extraction_ts = "2026-09-06 00:00:00"
    metadata_manager.update_and_save(
        entity="sessions",
        metadata_filename="bronze_metadata.json",
        set_metadata={"last_extraction_ts": new_last_extraction_ts}
    )

    # Get the metadata for sessions and print it
    sessions_metadata = metadata_manager.get_metadata(entity="sessions")
    print(f"Metadata for 'sessions': {sessions_metadata}")