from src.extract.extract_customers import extract_customers
from src.extract.extract_locations import extract_locations
from src.extract.extract_products import extract_products
from src.extract.extract_sessions import extract_sessions


def run_bronze_ingestion() -> dict:
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
        result = extraction_function()
        # if result:
        #     print(f"{entity.capitalize()} extraction complete!")
        #     print(result)
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
        if result:
            print(f"{entity.capitalize()}: {result['record_count']} records")
        else:
            print(f"{entity.capitalize()}: No data extracted.")
    print("_" * len(summary_title))
    print(f"TOTAL RECORDS: {total_records}")
    print("=" * len(summary_title))

if __name__ == "__main__":
    ingestion_results = run_bronze_ingestion()
    print_summary(ingestion_results)