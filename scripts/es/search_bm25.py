from elasticsearch import Elasticsearch
from pyserini.search import get_topics
from tqdm import tqdm

client = Elasticsearch("http://localhost:9200", timeout=60)
topics = get_topics("msmarco-passage-dev-subset")

def escape_query(query):
    escaped = ""
    for c in query:
        if c not in ['+', '-', '=', '&&', '||', '>', '<', '!', '(', ')', '{', '}', '[', ']', '^', '"', '~', '*', '?', ':', '\\', '/']:
            escaped += c
        else:
            escaped += f'\{c}'
    return escaped
    
with open('run.es_bm25.tsv', 'w') as f:
    for qid in tqdm(topics):
        query = escape_query(topics[qid]['title'])
        formated_query = {
            "query_string": {
                "query": query,
                "default_field": "document"
            }
        }
        resp = client.search(index="example_index", query=formated_query, timeout="60s")
        for i in range(len(resp["hits"]["hits"])):
            pid = resp["hits"]["hits"][i]['_id']
            record = f"{qid}\t{pid}\t{i+1}\n"
            f.write(record)

"""
#####################
MRR @10: 0.18397376859053075
QueriesRanked: 6980
#####################
"""