# Pyserini: REST API Server with FastAPI

The Pyserini FastAPI server provides a RESTful HTTP interface to Pyserini's search capabilities. 

## Starting the Server

You can start the FastAPI server by running the command:

```bash
python -m pyserini.server.rest
```

The server will start on [`http://localhost:8081/`](http://localhost:8081/) by default. You can specify a different port using the `--port` argument:

```bash
python -m pyserini.server.rest --port 8080
```

### Interactive API Documentation

Once the server is running, you can access the interactive API documentation with Swagger UI at `/docs`. 
For example, if you're running the rest server on port 8081, then go to [`http://localhost:8081/docs`](http://localhost:8081/docs).

## API Endpoints

The FastAPI server provides several endpoints for interacting with Pyserini indexes, some of which are shown below:

### 1. Search Index

**Endpoint:** `GET v1/indexes/{index}/search`

Perform a search query on the specified index.

**Example Request:**

```bash
curl "http://localhost:8081/v1/indexes/msmarco-v1-passage/search?query=what%20is%20a%20lobster%20roll&hits=1"
```

**Example Response:**

```json
{
  "query": {
    "qid": "",
    "text": "what is a lobster roll"
  },
  "candidates": [
    {
      "docid": "7157707",
      "score": 11.0082998275757,
      "doc": "Cookbook: Lobster roll Media: Lobster roll A lobster-salad style roll from The Lobster Roll in Amagansett, New York on the Eastern End of Long Island A lobster roll is a fast-food sandwich native to New England made of lobster meat served on a grilled hot dog-style bun with the opening on the top rather than the side. The filling may also contain butter, lemon juice, salt and black pepper, with variants made in other parts of New England replacing the butter with mayonnaise. Others contain diced celery or scallion. Potato chips or french fries are the typical sides."
    }
  ]
}
```

### 2. Get Document

**Endpoint:** `GET v1/indexes/{index}/documents/{docid}`

Retrieve a specific document by its document ID.

**Example Request:**

```bash
curl "http://localhost:8081/v1/indexes/msmarco-v1-passage/documents/7157715"
```

**Example Response:**

```json
{
  "docid": "7157715",
  "text": "A Lobster Roll is a bread roll filled with bite-sized chunks of lobster meat. Lobster Rolls are made on the Atlantic coast of North America, from the New England area of the United States on up into the Maritimes areas of Canada."
}
```

For all endpoints see the Swagger UI documentation.