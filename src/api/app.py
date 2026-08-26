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
    return {
        "status": "healthy"
    }

# ------------------- #
#  Session Endpoints  #
# ------------------- #

@app.get("/sessions")
def get_sessions():
    return STORE.get_sessions()

@app.get("/sessions/count")
def get_session_counts():
    return {
        "count": STORE.count()
    }

@app.get("/sessions/since/{timestamp}")
def get_sessions_since(timestamp: str):
    try:
        sessions = STORE.get_sessions_since(timestamp)

        return {
            "requested_timestamp": timestamp,
            "session_count": len(sessions),
            "sessions": sessions,
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
    if count <= 0:
        raise HTTPException(
            status_code=400,
            detail="Count must be greater than zero."
        )

    STORE.populate(count)

    return {
        "new_total_sessions": STORE.count()
    }

# ------------------- #
#   Reference Store   #
# ------------------- #
references = ReferenceStore()

@app.get("/products")
def get_products():
    return references.reference["products"]()

@app.get("/users")
def get_users():
    return references.reference["users"]()

@app.get("/locations")
def get_locations():
    return references.reference["locations"]()