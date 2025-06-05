from fastapi import FastAPI

from routes import search, indexes

# TODO: add to pyproject.toml

name = "Pyserini API"
version = "0.0.1"
description = "REST API for Pyserini functionality"


app = FastAPI(
    title=name,
    version=version,
    description=description
)

# Include routers
app.include_router(search.router)
app.include_router(indexes.router)

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": name,
        "version": version,
        "description": description,
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
    