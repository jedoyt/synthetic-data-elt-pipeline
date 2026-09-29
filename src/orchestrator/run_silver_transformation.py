from src.transform.transform_customers import transform_customers
from src.transform.transform_locations import transform_locations
from src.transform.transform_products import transform_products
from src.transform.transform_sessions import transform_sessions


def run_silver_transformations():
    """
    Run the Silver transformation process for all Bronze reference and session data.
    : return: A dictionary containing the results of the ingestion process for each entity.
    : rtype: dict
    """
    # Transformation and results
    result_customers = transform_customers()
    result_products = transform_products()
    result_locations = transform_locations()
    result_sessions, result_session_events = transform_sessions()

    return {
        'customers': result_customers,
        'products': result_products,
        'locations': result_locations,
        'sessions': result_sessions,
        'session events': result_session_events
    }

def print_summary(results: dict):
    """
    Print a summary of the Silver transformation process.
    : param results: dict - A dictionary containing the results of the transformation process for each entity.
    """
    summary_title = "\nSilver Transformation Summary:"
    total_records = sum(result['record_count'] for result in results.values() if result)
    print("_" * len(summary_title))
    print(summary_title)
    print("=" * len(summary_title))
    for entity, result in results.items():
        print(f"{entity.capitalize()}: {result['record_count']} records")
    print("_" * len(summary_title))
    print(f"TOTAL RECORDS: {total_records}")
    print("=" * len(summary_title))

if __name__ == '__main__':
    print("SILVER TRANSFORMATION STARTED...")

    # Run Silver Transformation
    transformation_results = run_silver_transformations()
    print_summary(transformation_results)