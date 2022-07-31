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
