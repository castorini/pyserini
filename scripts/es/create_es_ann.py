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

# Create the client instance
client = Elasticsearch("http://localhost:9200", timeout=1000)
print(client.info())

ann_index_config = {
    "mappings": {
        "properties": {
            "text-vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "dot_product",
            },
        }
    }
}

client.indices.create(index='es-hnsw', body=ann_index_config)
