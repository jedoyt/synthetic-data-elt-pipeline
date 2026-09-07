from datetime import UTC, datetime
from urllib.parse import quote

from fastapi import FastAPI, HTTPException

from src.api.event_store import EventStore
from src.api.reference_store import ReferenceStore

# ------------------ #
# App Initialization #
# ------------------ #
app = FastAPI(
    title="Synthetic E-Commerce Analytics API",
    description="Pseudo REST API that exposes synthetic session data "
                "for ELT pipeline development",
    version="0.1.0"
)

# ------------------ #
#     Event Store    #
# ------------------ #

STORE = EventStore()

# Populate some sessions on startup
STORE.populate(100)

# ------------------ #
#    Health Check    #
# ------------------ #

@app.get("/health")
def health():
    """Return the service health status."""
    return {
        "status": "healthy"
    }

# ------------------- #
#  Session Endpoints  #
# ------------------- #
@app.get("/")
def index():
    """Return a welcome message for the API root endpoint."""
    return {"message": f"Welcome to {app.title}!"}

@app.get("/sessions")
def get_sessions():
    """Return all sessions currently held by the event store."""
    # return STORE.get_sessions()
    return {
        "request_timestamp": datetime.now(UTC).isoformat(),
        "endpoint": "/sessions",
        "record_count": STORE.count(),
        "records": STORE.get_sessions(),
    }

@app.get("/sessions/count")
def get_session_counts():
    """Return the number of sessions currently held by the event store."""
    # return {
    #     "count": STORE.count()
    # }
    return {
        "request_timestamp": datetime.now(UTC).isoformat(),
        "endpoint": "/sessions/count",
        "record_count": STORE.count(),
        "records": [],
    }

@app.get("/sessions/since/{timestamp}")
def get_sessions_since(timestamp: str):
    """Return sessions whose start time is later than the requested timestamp."""
    try:
        sessions = STORE.get_sessions_since(timestamp)

        return {
            "request_timestamp": timestamp,
            "endpoint": f"/sessions/since/{quote(timestamp)}",
            "record_count": len(sessions),
            "records": sessions,
        }
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid timestamp."
                "Use ISO-8601 format."
            )
        )

# ---------------------------- #
# Development / Debug Endpoint #
# ---------------------------- #

@app.post("/sessions/generate/{count}")
def generate_more_sessions(count: int):
    """Generate and store the requested number of additional sessions."""
    if count <= 0:
        raise HTTPException(
            status_code=400,
            detail="Count must be greater than zero."
        )

    STORE.populate(count)

    # return {"new_total_sessions": STORE.count()}
    return {
        "request_timestamp": datetime.now(UTC).isoformat(),
        "endpoint": f"/sessions/generate/{count}",
        "record_count": STORE.count(),
        "records": [],
    }

# ------------------- #
#   Reference Store   #
# ------------------- #
references = ReferenceStore()

@app.get("/products")
def get_products():
    """Return the product reference data."""
    PRODUCTS = references.fetch_products()
    # return references.fetch_products()
    return {
        "request_timestamp": datetime.now(UTC).isoformat(),
        "endpoint": "/products",
        "record_count": len(PRODUCTS),
        "records": PRODUCTS,
    }

@app.get("/customers")
def get_customers():
    """Return the customer reference data."""
    CUSTOMERS = references.fetch_customers()
    # return references.fetch_customers()
    return {
        "request_timestamp": datetime.now(UTC).isoformat(),
        "endpoint": "/customers",
        "record_count": len(CUSTOMERS),
        "records": CUSTOMERS,
    }

@app.get("/locations")
def get_locations():
    """Return the location reference data."""
    LOCATIONS = references.fetch_locations()
    # return references.fetch_locations()
    return {
        "request_timestamp": datetime.now(UTC).isoformat(),
        "endpoint": "/locations",
        "record_count": len(LOCATIONS),
        "records": LOCATIONS,
    }