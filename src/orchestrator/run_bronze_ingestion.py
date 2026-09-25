from src.extract.extract_customers import extract_customers
from src.extract.extract_locations import extract_locations
from src.extract.extract_products import extract_products
from src.extract.extract_sessions import extract_sessions


def run_bronze_ingestion(since_ts=None) -> dict:
    """
    Run the Bronze ingestion process for all reference and session data.
    : return: A dictionary containing the results of the ingestion process for each entity.
    : rtype: dict
    """
    extractor_dict = {
        "customers": extract_customers,
        "products": extract_products,
        "locations": extract_locations,
        "sessions": extract_sessions,
    }
    results = {}
    for entity, extraction_function in extractor_dict.items():
        print(f"Starting extraction for {entity}...")
        if extraction_function == extract_sessions:
            result = extraction_function(since_ts=since_ts)
        else:
            result = extraction_function()
        results[entity] = result
    return results

def print_summary(results: dict):
    """
    Print a summary of the Bronze ingestion process.
    : param results: dict - A dictionary containing the results of the ingestion process for each entity.
    """
    summary_title = "\nBronze Ingestion Summary:"
    total_records = sum(result['record_count'] for result in results.values() if result)
    print("_" * len(summary_title))
    print(summary_title)
    print("=" * len(summary_title))
    for entity, result in results.items():
        print(f"{entity.capitalize()}: {result['record_count']} records")
    print("_" * len(summary_title))
    print(f"TOTAL RECORDS: {total_records}")
    print("=" * len(summary_title))


# Test run_bronze_ingestion
if __name__ == "__main__":
    print("BRONZE INGESTION STARTED...")
    since_ts = input("Enter a watermark timestamp for sessions (ISO format), or press Enter for full extraction:\n")

    if since_ts:
        # Run Bronze ingestion with the current timestamp as the watermark for sessions
        from datetime import UTC, datetime
        ingestion_results = run_bronze_ingestion(since_ts=datetime.now(UTC).isoformat())
        print_summary(ingestion_results)
    else:
        # Run Bronze ingestion at full extraction
        ingestion_results = run_bronze_ingestion(since_ts=None)
        print_summary(ingestion_results)