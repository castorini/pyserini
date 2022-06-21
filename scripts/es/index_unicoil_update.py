#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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