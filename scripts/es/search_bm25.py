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
        resp = client.search(index="msmarco-v1-passage", query=formated_query, timeout="60s")
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