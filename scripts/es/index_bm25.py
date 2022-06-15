import json
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from tqdm import tqdm

INDEX_NAME = "msmarco-v1-passage"
MSMARCO_PATH = 'data/msmarco-passage-unicoil/'


def generate_msmarco_passage():
    for file in os.listdir(MSMARCO_PATH):
        path = os.path.join(MSMARCO_PATH, file)
        with open(path) as f:
            for line in f:
                info = json.loads(line)
                docid = info['id']
                text = info['contents']
                action = {
                    "_index": INDEX_NAME,
                    "_id": docid,
                    "document": text
                }
                yield action

client = Elasticsearch("http://localhost:9200")


print("Indexing documents...")
successes = 0
for ok, action in tqdm(streaming_bulk(
    client=client, index=INDEX_NAME, actions=generate_msmarco_passage(),
)):
    successes += ok
print(f"Indexed {successes} documents")