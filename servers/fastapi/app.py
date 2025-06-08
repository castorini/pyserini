"""
FastAPI Server for Pyserini

Launches a REST API server for Pyserini search functionality.

Usage:
    python app.py [--port PORT]

Example:
    python app.py --port 5000

Endpoints:
    GET /                 : API metadata and documentation link.
    /indexes/*            : Index search, document, status, and settings endpoints (see routers).
    /docs                 : Swagger UI for API documentation.

"""

from fastapi import FastAPI
import sys
from pathlib import Path

# Ensure the parent directory is in sys.path for module resolution
sys.path.append(str(Path(__file__).resolve().parent.parent))

from routes.indexes import router


name = "Pyserini API"
version = "0.0.1"
description = "REST API for Pyserini functionality"

app = FastAPI(title=name, version=version, description=description)

# Include routers
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": name,
        "version": version,
        "description": description,
        "documentation": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description="Run the Pyserini API server.")
    parser.add_argument('--port', type=int, default=8081, help='Port to run the server on (default: 8081)')
    args = parser.parse_args()

    uvicorn.run(app, host="0.0.0.0", port=args.port)
