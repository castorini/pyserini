from elasticsearch import Elasticsearch

# Create the client instance
client = Elasticsearch("http://localhost:9200")
print(client.info())

impact_index_config = {
    "settings": {
        "number_of_shards": 1,
        "similarity": {
            "default": {
                "type": "BM25",
                "k1": 0.9,
                "b": 0.4
            },
            "impact_similarity": {
                "type": "scripted",
                "script": {
                    "source": "double tf = doc.freq; return query.boost * tf;"
                }
            },
        }
    },
    "mappings": {
        "properties": {
            "document": {
                "type": "text",
                "analyzer": "english",
                "similarity": "default",
            },
            "vector": {
                "type": "text",
                "analyzer": "whitespace",
                "similarity": "impact_similarity"
            }
        }
    }
}

client.indices.create(index='msmarco-v1-passage', body=impact_index_config)

