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
client = Elasticsearch("http://localhost:9200")
print(client.info())

impact_index_config = {
    "settings": {
        "number_of_shards": 1,
        "similarity": {
            "default": {
                "type": "BM25",
                "k1": 0.9,
                "b": 0.4
            },
            "impact_similarity": {
                "type": "scripted",
                "script": {
                    "source": "double tf = doc.freq; return query.boost * tf;"
                }
            },
        }
    },
    "mappings": {
        "properties": {
            "document": {
                "type": "text",
                "analyzer": "english",
                "similarity": "default",
            },
            "vector": {
                "type": "text",
                "analyzer": "whitespace",
                "similarity": "impact_similarity"
            }
        }
    }
}

client.indices.create(index='msmarco-v1-passage', body=impact_index_config)

