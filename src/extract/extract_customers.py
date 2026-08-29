from src.extract.api_client import APIClient
from src.extract.bronze_writer import BronzeWriter

# Localhost URL
URL_PREFIX = "http://127.0.0.1:8000"

def extract_customers():

    client = APIClient(url_prefix=URL_PREFIX)
    writer = BronzeWriter()

    customers = client.get("/customers")

    result = writer.write_jsonl(
        records=customers["data"],
        entity_name="customers"
    )

    return result


# Test extract_customers
if __name__ == "__main__":

    result = extract_customers()

    print("Customer extraction complete")
    print(result)