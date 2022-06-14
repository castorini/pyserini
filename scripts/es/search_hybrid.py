from elasticsearch import Elasticsearch
from pyserini.search import get_topics
from tqdm import tqdm

client = Elasticsearch("http://localhost:9200", timeout=60)
topics = get_topics("msmarco-passage-dev-subset")
topics_unicoil = get_topics("msmarco-passage-dev-subset-unicoil")


def escape_query(query):
    escaped = ""
    for c in query:
        if c not in ['+', '-', '=', '&&', '||', '>', '<', '!', '(', ')', '{', '}', '[', ']', '^', '"', '~', '*', '?', ':', '\\', '/']:
            escaped += c
        else:
            escaped += f'\{c}'
    return escaped


def convert_pseudo_query_to_boost(query):
    tf = {}
    tokens = query.split()
    for tok in tokens:
        if tok not in tf:
            tf[tok] = 0
        tf[tok] += 1
    boost = ""
    for tok in tf:
        if tok != "[SEP]":
            escaped = tok
            if tok in ['+', '-', '=', '&&', '||', '>', '<', '!', '(', ')', '{', '}', '[', ']', '^', '"', '~', '*', '?', ':', '\\', '/']:
                escaped = tok.replace(tok, f"\\{tok}")
            boost += f"{escaped}^{tf[tok]} "
    return boost.rstrip()


with open('run.es_hybrid.tsv', 'w') as f:
    for qid in tqdm(topics):
        query_bm25 = escape_query(topics[qid]['title'])
        query_unicoil = convert_pseudo_query_to_boost(
            topics_unicoil[qid]['title'])
        formated_query = {
            "bool": {
                "should": [
                    {"query_string": {
                        "query": query_unicoil,
                        "default_field": "vector",
                        "boost": 1
                    }},
                    {"query_string": {
                        "query": query_bm25,
                        "default_field": "document",
                        "boost": 1
                    }},
                ]
            }
        }
        resp = client.search(index="example_index", query=formated_query)
        for i in range(len(resp["hits"]["hits"])):
            pid = resp["hits"]["hits"][i]['_id']
            record = f"{qid}\t{pid}\t{i+1}\n"
            f.write(record)
