from elasticsearch import Elasticsearch
from pyserini.search import get_topics, QueryEncoder
from tqdm import tqdm

client = Elasticsearch("http://localhost:9200", timeout=1000)
topics = get_topics("msmarco-passage-dev-subset")
query_encoder = QueryEncoder.load_encoded_queries('sbert-msmarco-passage-dev-subset')
with open('run.es_sbert.tsv', 'w') as f:
    for qid in tqdm(topics):
        query = topics[qid]['title']
        formated_query = {
                "field": "text-vector",
                "query_vector": query_encoder.encode(query),
                "k": 10,
                "num_candidates": 100
        }
        resp = client.knn_search(index="tct-colbert-hnsw", knn=formated_query)
        for i in range(len(resp["hits"]["hits"])):
            pid = resp["hits"]["hits"][i]['_id']
            record = f"{qid}\t{pid}\t{i+1}\n"
            f.write(record)