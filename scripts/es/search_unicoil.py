from elasticsearch import Elasticsearch
from pyserini.search import get_topics
from tqdm import tqdm

client = Elasticsearch("http://localhost:9200")
topics = get_topics("msmarco-passage-dev-subset-unicoil")


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


with open('run.es_unicoil.tsv', 'w') as f:
    for qid in tqdm(topics):
        query = convert_pseudo_query_to_boost(topics[qid]['title'])
        formated_query = {
            "query_string": {
                "query": query,
                "default_field": "vector"
            }
        }
        resp = client.search(index="msmarco-v1-passage", query=formated_query)
        for i in range(len(resp["hits"]["hits"])):
            pid = resp["hits"]["hits"][i]['_id']
            record = f"{qid}\t{pid}\t{i+1}\n"
            f.write(record)


"""
#####################
MRR @10: 0.35155222404147773
QueriesRanked: 6980
#####################
"""