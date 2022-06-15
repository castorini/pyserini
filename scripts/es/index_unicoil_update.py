import json
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from tqdm import tqdm

INDEX_NAME = "msmarco-v1-passage"
MSMARCO_PATH = 'data/msmarco-passage-unicoil/'

def create_pseudo_doc(vector):
    results = []
    for key in vector:
        results += [key] * vector[key]
    pesudo_doc = " ".join(results)
    return pesudo_doc

def generate_unicoil_vector():
    for file in os.listdir(MSMARCO_PATH):
        path = os.path.join(MSMARCO_PATH, file)
        with open(path) as f:
            for line in f:
                info = json.loads(line)
                docid = info['id']
                text = create_pseudo_doc(info['vector'])
                action = {
                    "_op_type": "update",
                    "_index": INDEX_NAME,
                    "_id": docid,
                    "doc": {"vector": text},
                }
                yield action

client = Elasticsearch("http://localhost:9200")


print("Indexing documents...")
successes = 0
for ok, action in tqdm(streaming_bulk(
    client=client, index=INDEX_NAME, actions=generate_unicoil_vector(),
)):
    successes += ok
print(f"Indexed {successes} documents")