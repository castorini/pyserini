from elasticsearch import Elasticsearch

# Create the client instance
client = Elasticsearch("http://localhost:9200")

resp = client.search(index="msmarco-v1-passage", query={"bool": {
    "must_not": {
        "exists": {
            "field": "vector"
        }
    }
}}, track_total_hits=True)

print(resp['hits']['total']['value'])
