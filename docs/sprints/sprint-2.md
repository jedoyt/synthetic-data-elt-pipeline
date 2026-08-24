# Sprint 2: Pseudo REST API + Bronze Ingestion
## Learning Goal
Learn how analytical systems consume operational system data.

We'll deliberately separate producer from consumer for the first time.

## Why Sprint 2 Matters?
Right now `generate_session()` is called directly.

But in reality, the pipeline shouldn't know how sessions are generated.
It should simply call endpoint, receive JSON, persist raw data.
```
Operational System
        ↓
API Layer
        ↓
Data Pipeline
```

## Target Architecture
```
EPOS
(Session Generator)
        ↓
Pseudo REST API
        ↓
Extractor
        ↓
Bronze JSONL
        ↓
Metadata Tracking
```

## Sprint 2 Deliverables:
- In-memory event store
      * `src/api/event_store.py`
      * Responsibilities:
            - Generate Sessions
            - Hold sessions in memory
            - Provide retrieval functions
- Pseudo REST API (using FastAPI)
      * `src/api/app.py`
      * Endpoint 1, GET /health
      * Endpoint 2, GET /sessions
      * Endpoint 3, GET /session?since=<timestamp>
- Extractor
      * `src/extract/extract_sessions.py`
      * Responsibilities
            - Call PI
            - Receive sessions
            - Return list
- Bronze Layer
      * `data/bronze/`
      * in `.jsonl` format
- Metadata Tracking
      * `metadata.sqlite`
      * `pipeline_metadata.json`
- Folder Structure
```text
src/

├── api/
│   ├── app.py
│   └── event_store.py

├── extract/
│   └── extract_sessions.py

├── metadata/
│   └── metadata_manager.py
```

## Acceptance Criteria
1. `python app.py` launches the API
2. `python extract_session.py`
      - produces 25 sessions extracted
      - bronze file created
      - watermark updated
      - creates:
            * `data/bronze/`
            * `session_*.jsonl`

## What Sprint 2 will teach
- Source Systems
- API Contracts
- Data Ingestion
- Bronze Architecture
- Incremental Extraction
- Metadata Tracking
- Raw Data Preservation