"""
FastAPI Server for Pyserini

Launches a REST API server for Pyserini search functionality. Optional arg for port number.

Usage:
    python -m pyserini.server.rest [--port PORT]

Example:
    python -m pyserini.server.rest --port 8080

Endpoints:
    GET /                 : API metadata and documentation link.
    /indexes/*            : Index search, document, status, and settings endpoints (see routers).
    /docs                 : Swagger UI for API documentation.

"""

from fastapi import FastAPI
from pyserini.server.rest.routes.indexes import router


SERVER_NAME = 'Pyserini API'
VERSION = 'v1'
DESCRIPTION = 'REST API for Pyserini functionality'

app = FastAPI(title=SERVER_NAME, version=VERSION, description=DESCRIPTION)

# Include routers
app.include_router(router, prefix=f'/{VERSION}')


@app.get('/')
async def root():
    """Root endpoint with API information."""
    return {
        'name': SERVER_NAME,
        'version': VERSION,
        'description': DESCRIPTION,
        'documentation': '/docs',
    }


def main():
    """Main function to run the FastAPI server."""
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description='Run the Pyserini API server.')
    parser.add_argument(
        '--port',
        type=int,
        default=8081,
        help='Port to run the server on (default: 8081)',
    )
    args = parser.parse_args()

    uvicorn.run(app, host='0.0.0.0', port=args.port)
