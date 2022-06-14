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

# client.indices.create(index='example_index', body=impact_index_config)

# doc = {
#     'document': 'where is university of waterloo'
# }

# vec = {
#     'vector': 'where is university of waterloo waterloo waterloo waterloo'
# }
# resp = client.update(index="example_index", id=1, doc=doc)
# resp = client.update(index="example_index", id=2, doc=doc)
# resp = client.update(index="example_index", id=1, doc=vec)
#print(client.get(index="example_index", id=3))
client.indices.refresh(index="example_index")

# query = {
#     "query": {
#         "dis_max": {
#             "queries": [
#                 {"match": {"document": "waterloo's"}},
#                 {"match": {"vector": "waterloo's"}}
#             ]
#         }
#     }
# }

resp = client.search(index="example_index", query={"bool": {
    "must_not": {
        "exists": {
            "field": "vector"
        }
    }
}}, track_total_hits=True)
print(resp['hits']['total'])
