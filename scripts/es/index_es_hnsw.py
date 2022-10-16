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
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from tqdm import tqdm
import faiss

INDEX_NAME = "es-hnsw"
MSMARCO_PATH = '<path-to>/dindex-msmarco-passage-sbert-bf-20210313-a0fbb3/'

bf_index = faiss.read_index(os.path.join(MSMARCO_PATH, 'index'))
vectors = bf_index.reconstruct_n(0, bf_index.ntotal)
docids = [x.rstrip() for x in open(os.path.join(MSMARCO_PATH, 'docid')).readlines()]

def generate_msmarco_passage():
    for idx in range(len(vectors)):
        docid = docids[idx]
        vector = vectors[idx]
        action = {
            "_index": INDEX_NAME,
            "_id": docid,
            "text-vector": vector
        }
        yield action

client = Elasticsearch("http://localhost:9200", timeout=1000)


print("Indexing documents...")
successes = 0
for ok, action in tqdm(streaming_bulk(
    client=client, index=INDEX_NAME, actions=generate_msmarco_passage(),
)):
    successes += ok
print(f"Indexed {successes} documents")
